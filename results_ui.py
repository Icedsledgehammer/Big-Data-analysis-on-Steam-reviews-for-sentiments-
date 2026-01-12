from flask import Flask, render_template_string
import subprocess
import re

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
  <title>Steam Sentiment Analysis</title>
  <style>
    body { font-family: Arial; text-align: center; margin: 50px; background: #f4f4f9; }
    h1 { color: #2c3e50; }
    .box { background: white; padding: 20px; margin: 20px auto; width: 60%; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    .metric { font-size: 28px; font-weight: bold; color: #e74c3c; }
    .good { color: #27ae60; }
    table { margin: 20px auto; border-collapse: collapse; }
    th, td { padding: 12px; border: 1px solid #ddd; }
    th { background: #3498db; color: white; }
  </style>
</head>
<body>
  <h1>Steam Review Sentiment Analysis</h1>
  <div class="box">
    <p><span class="metric">AUC: {{ auc }}</span></p>
    <p><span class="metric good">Accuracy: {{ accuracy }}%</span></p>
  </div>
  <div class="box">
    <h2>Confusion Matrix</h2>
    <table>
      <tr><th></th><th>Pred Neg</th><th>Pred Pos</th></tr>
      <tr><th>True Neg</th><td>{{ tn }}</td><td>{{ fp }}</td></tr>
      <tr><th>True Pos</th><td>{{ fn }}</td><td>{{ tp }}</td></tr>
    </table>
  </div>
  <div class="box">
    <p><strong>HDFS Data:</strong> {{ hdfs_size }}</p>
    <p><strong>MongoDB Docs:</strong> {{ mongo_count }}</p>
    <p><strong>Model:</strong> ~/sentiment_model_final</p>
  </div>
  <p><em>Live Demo — Hadoop + Mahout + MongoDB</em></p>
</body>
</html>
'''

@app.route('/')
def home():
    # Default values
    auc = "N/A"
    tn = fp = fn = tp = 0
    accuracy = 0
    hdfs_size = "N/A"
    mongo_count = "N/A"

    try:
        # Run Mahout test
        result = subprocess.run([
            'mahout', 'runlogistic',
            '--input', '/home/icedsledgehammer/test_balanced_fixed.csv',
            '--model', '/home/icedsledgehammer/sentiment_model_final',
            '--auc', '--confusion'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30)

        for line in result.stdout.split('\n'):
            if 'AUC' in line:
                auc = line.split('=')[1].strip()
            if 'confusion' in line:
                nums = re.findall(r'\d+\.?\d*', line)
                if len(nums) == 4:
                    tn, fp, fn, tp = [float(x) for x in nums]
                    total = tn + fp + fn + tp
                    accuracy = round((tn + tp) / total * 100, 1) if total > 0 else 0

        # HDFS size
        hdfs = subprocess.run(
            ['hdfs', 'dfs', '-du', '-h', '/user/sentiment_project/'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )
        lines = [line for line in hdfs.stdout.split('\n') if line.strip() and not line.startswith('#')]
        hdfs_size = lines[0].split()[0] if lines else "N/A"

        # MongoDB count - extract only the number
        mongo = subprocess.run([
            'mongo', '--username', 'admin', '--password', 'newpassword123',
            '--authenticationDatabase', 'admin', '--eval',
            'db.steam_features.count()', 'sentiment_db'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        mongo_count = "N/A"
        for line in mongo.stdout.split('\n'):
            line = line.strip()
            if line.isdigit():
                mongo_count = line
                break

    except Exception as e:
        auc = f"Error: {str(e)}"

    return render_template_string(HTML,
        auc=auc, accuracy=accuracy,
        tn=tn, fp=fp, fn=fn, tp=tp,
        hdfs_size=hdfs_size, mongo_count=mongo_count
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
