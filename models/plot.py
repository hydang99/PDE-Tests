
import matplotlib.pyplot as plt
import re



with open('logs_baseline.txt', 'r') as f:
    data = f.read()

train_loss = re.findall(r" loss: (0\.\d+)", data)
val_loss = re.findall(r" val_loss: (0\.\d+)", data)

train_loss = list(map(lambda x : float(x), train_loss))[:48]
val_loss = list(map(lambda x : float(x), val_loss))[:48]

plt.plot(train_loss, "r--", color="r", label='Train Loss')
plt.plot(val_loss, "r--", color="b", label='Val Loss')

plt.title("Log Loss")
plt.legend()
plt.show()