"""
Packaging-metadata unit test — TD 239 item #1 (dev-deps split).

Verifies that setup.py's computed ``install_requires`` (derived from requirements.txt
via parse_requirements) contains ONLY the 5 runtime dependencies and none of the dev /
release packages. This guards against dev tooling leaking into end-user ``pip install``.
"""
import os
import sys
import types
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
SETUP_PY = os.path.join(REPO_ROOT, "setup.py")

# Dev / release-only packages that must NOT appear in install_requires.
_DEV_PACKAGES = (
    "python-dotenv",
    "pytest",
    "pytest-asyncio",
    "pytest-cov",
    "ruff",
    "build",
    "twine",
)
_RUNTIME_PACKAGES = (
    "httpx",
    "requests",
    "websockets",
    "certifi",
    "loguru",
)


def _capture_install_requires():
    """Execute setup.py with a stub ``setuptools`` module, capturing install_requires.

    setuptools may not be importable in the runtime test environment (it is only
    needed at build time), so we inject a lightweight stub that records the
    ``setup(**kwargs)`` call and provides a no-op ``find_packages``.
    """
    captured = {}

    def _fake_setup(**kwargs):
        captured.update(kwargs)

    stub = types.ModuleType("setuptools")
    stub.setup = _fake_setup
    stub.find_packages = lambda *args, **kwargs: []

    original = sys.modules.get("setuptools")
    sys.modules["setuptools"] = stub
    cwd = os.getcwd()
    os.chdir(REPO_ROOT)
    try:
        with open(SETUP_PY, "r", encoding="utf-8") as fh:
            source = fh.read()
        # Run setup.py in an isolated namespace anchored at the repo root so its
        # relative reads (requirements.txt, README.md) resolve correctly.
        exec(compile(source, SETUP_PY, "exec"), {"__file__": SETUP_PY, "__name__": "setup"})
    finally:
        os.chdir(cwd)
        if original is not None:
            sys.modules["setuptools"] = original
        else:
            sys.modules.pop("setuptools", None)
    return captured.get("install_requires", [])


def _base_name(requirement):
    """Strip version specifiers and extras: 'httpx[http2]>=0.24.0' -> 'httpx'."""
    for sep in (">=", "<=", "==", "~=", "!=", ">", "<", "["):
        idx = requirement.find(sep)
        if idx != -1:
            requirement = requirement[:idx]
    return requirement.strip().lower()


class TestPackagingInstallRequires(unittest.TestCase):
    def setUp(self):
        self.install_requires = _capture_install_requires()
        self.base_names = {_base_name(r) for r in self.install_requires}

    def test_no_dev_package_in_install_requires(self):
        for pkg in _DEV_PACKAGES:
            self.assertNotIn(
                pkg.lower(), self.base_names,
                msg=f"dev package '{pkg}' leaked into install_requires: {self.install_requires}",
            )

    def test_runtime_packages_present(self):
        for pkg in _RUNTIME_PACKAGES:
            self.assertIn(
                pkg, self.base_names,
                msg=f"runtime package '{pkg}' missing from install_requires: {self.install_requires}",
            )

    def test_exactly_five_runtime_deps(self):
        self.assertEqual(
            len(self.install_requires), 5,
            msg=f"expected exactly 5 runtime deps, got: {self.install_requires}",
        )


if __name__ == "__main__":
    unittest.main()
