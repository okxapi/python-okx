import pickle

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import pandas as pd

from myWork.model.prepare_data import prepare_training_data


# 假设prepare_training_data函数已经定义

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size, dropout=0.2):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # LSTM层
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )

        # 全连接层
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 50),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(50, output_size)
        )

    def forward(self, x):
        # 初始化隐藏状态和细胞状态
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        # LSTM前向传播
        out, _ = self.lstm(x, (h0, c0))

        # 只取序列中的最后一个时间步的输出
        out = self.fc(out[:, -1, :])
        return out


def train_lstm_model(X_train, y_train, X_test, y_test,
                     input_size, hidden_size=64, num_layers=2, output_size=1,
                     batch_size=64, epochs=50, lr=0.001, device='cuda'):
    """训练LSTM模型并返回训练好的模型和训练历史"""
    # 转换为PyTorch张量
    X_train_tensor = torch.FloatTensor(X_train).to(device)
    y_train_tensor = torch.FloatTensor(y_train).to(device)
    X_test_tensor = torch.FloatTensor(X_test).to(device)
    y_test_tensor = torch.FloatTensor(y_test).to(device)

    # 创建数据加载器
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # 初始化模型
    model = LSTMModel(input_size, hidden_size, num_layers, output_size).to(device)
    model.load_state_dict(torch.load('best_lstm_model.pth'))

    # 定义损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5, factor=0.5)

    # 训练历史记录
    train_losses = []
    val_losses = []
    best_val_loss = float('inf')

    for epoch in range(epochs):
        print("開始訓練")
        model.train()
        train_loss = 0
        for X_batch, y_batch in train_loader:
            # 前向传播
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)

            # 反向传播和优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * X_batch.size(0)

        # 验证
        model.eval()
        with torch.no_grad():
            val_outputs = model(X_test_tensor)
            val_loss = criterion(val_outputs, y_test_tensor).item()

        # 记录损失
        train_loss = train_loss / len(train_loader.dataset)
        train_losses.append(train_loss)
        val_losses.append(val_loss)

        # 学习率调整
        scheduler.step(val_loss)

        # 保存最佳模型
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), 'best_lstm_model.pth')


        print(f'Epoch [{epoch + 1}/{epochs}], Train Loss: {train_loss:.6f}, Val Loss: {val_loss:.6f}')

    # 加载最佳模型
    model.load_state_dict(torch.load('best_lstm_model.pth'))

    return model, {'train_loss': train_losses, 'val_loss': val_losses}


def predict_with_model(model, X, scaler, device='cuda'):
    """使用训练好的模型进行预测并反标准化结果"""
    model.eval()
    with torch.no_grad():
        X_tensor = torch.FloatTensor(X).to(device)
        predictions = model(X_tensor).cpu().numpy()

    # 创建一个临时数组用于反标准化
    temp_array = np.zeros((predictions.shape[0], scaler.n_features_in_))
    # 假设'c'是第四列
    temp_array[:, 3] = predictions.flatten()
    # 反标准化
    temp_array = scaler.inverse_transform(temp_array)
    # 提取预测值
    predictions = temp_array[:, 3].reshape(-1, 1)

    return predictions


def plot_training_history(history):
    """绘制训练历史"""
    plt.figure(figsize=(10, 5))
    plt.plot(history['train_loss'], label='Train Loss')
    plt.plot(history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"history.png", dpi=300)


def plot_predictions(y_true, y_pred, title='Price Prediction'):
    """绘制预测结果与实际值对比图"""
    plt.figure(figsize=(12, 6))
    plt.plot(y_true, label='Actual Price')
    plt.plot(y_pred, label='Predicted Price')
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"prediction.png", dpi=300)


def main(file_path, lookback=60, forecast=1, split_ratio=0.8):
    # 准备数据
    X_train = np.load("X_train.npy")
    X_test = np.load("X_test.npy")
    y_train = np.load("y_train.npy")
    y_test = np.load("y_test.npy")

    # 加载scaler
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    # 加载DataFrame
    # df_processed = pd.read_parquet("df_processed.parquet")

    # 确定输入特征数量
    input_size = X_train.shape[2]

    # 设置设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')

    # 训练模型
    model, history = train_lstm_model(
        X_train, y_train, X_test, y_test,
        input_size=input_size,
        hidden_size=16,
        num_layers=2,
        output_size=forecast,
        batch_size=16,
        epochs=0,
        lr=0.001,
        device=device
    )
    #
    # # 绘制训练历史
    plot_training_history(history)

    # 在测试集上预测
    y_test_pred = predict_with_model(model, X_test, scaler, device)

    # 反标准化真实值
    temp_array = np.zeros((y_test.shape[0], scaler.n_features_in_))
    temp_array[:, 3] = y_test.flatten()
    y_test_true = scaler.inverse_transform(temp_array)[:, 3].reshape(-1, 1)

    # 绘制预测结果
    plot_predictions(y_test_true, y_test_pred, 'Test Set Price Prediction')

    # 计算评估指标
    mse = np.mean((y_test_pred - y_test_true) ** 2)
    mae = np.mean(np.abs(y_test_pred - y_test_true))
    mape = np.mean(np.abs((y_test_pred - y_test_true) / y_test_true)) * 100

    print(f"Test MSE: {mse:.4f}")
    print(f"Test MAE: {mae:.4f}")
    print(f"Test MAPE: {mape:.2f}%")

    return model, scaler


if __name__ == "__main__":
    # 使用示例
    file_path = "../sorted_history.csv"  # 替换为实际的K线数据文件路径
    model, scaler = main(file_path)
