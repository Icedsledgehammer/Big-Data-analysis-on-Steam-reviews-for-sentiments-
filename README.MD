# Steam Review Sentiment Analysis Pipeline

End-to-end **big data sentiment classification** project using the **Hadoop ecosystem** on a 2.14 GB subset of Steam game reviews.

### Live Demo Video
Watch a full end-to-end demo (Hadoop start → Pig processing → live Flask dashboard):  
🎥 [Demo Video (Google Drive link)](https://drive.google.com/file/d/1FBVuE9CgBSsA6btdHDr346Sm3RQXFfjc/view?usp=sharing)]
*(~2–3 minutes – shows jps, Pig job, MongoDB count, dashboard with AUC 0.55)*

### Key Results
- **Raw dataset**: 2.14 GB English Steam reviews (~6.4 million records)  
- **Cleaned records**: ~600,160 after filtering (length, duplicates, English only)  
- **Model**: Apache Mahout distributed logistic regression  
- **Performance** (balanced test set):  
  - AUC: **0.55**  
  - Accuracy: **53.4%**  
  (Realistic given noisy text, sarcasm, and 91% positive class bias)

### Tech Stack
- Hadoop 2.7.7 (HDFS + YARN)  
- Apache Pig 0.17 (cleaning + TF-IDF feature extraction)  
- MongoDB 4.4.29 (feature vector storage)  
- Apache Mahout 0.9 (distributed ML training)  
- Flask + Python 3.6 (real-time web dashboard)

### Project Structure
steam-sentiment-analysis/
├── pig_features.pig               # Pig Latin: cleaning + TF-IDF extraction
├── results_ui.py                  # Flask live dashboard
├── sentiment_model_final/         # Trained Mahout model folder
├── README.md
└── LICENSE

### Dataset
**Used dataset**: Steam Reviews (English-only subset)  
**Raw size**: 2.14 GB  
**Cleaned size**: ~600,160 records  
**Preprocessing**:
- Removed reviews < 10 words  
- Removed exact duplicates  
- Kept only English reviews  
- Binary label: `voted_up` (1 = positive, 0 = negative)

**Download**:  
[Steam Store Reviews – Kaggle (similar public source)](https://www.kaggle.com/datasets/nikdavis/steam-store-reviews)  
(Filter to English only if using full multilingual version)

### How to Reproduce (Local Pseudo-Distributed Mode)

1. **Start Hadoop + MongoDB**  
   Use your startup script or:
```bash
start-dfs.sh
start-yarn.sh
sudo systemctl start mongod
```

2. **Run Pig cleaning & feature extraction**
```bash
pig -f pig_features.pig
```

3. **(Optional) Import features to MongoDB**
```bash
hdfs dfs -get /user/sentiment_project/features_tfidf/part-r-00000 features.csv
mongoimport --db sentiment_db --collection steam_features --type csv --headerline --file features.csv
```

4. **Launch live dashboard**
```bash
python3 results_ui.py
```

→ Open: http://localhost:5000

### Why This Stack?
- **Pig**: Procedural style → ideal for step-by-step text ETL (tokenization, cleaning, TF-IDF)  
- **MongoDB**: Sub-second queries + flexible JSON → enables live dashboard  
- **Mahout**: Distributed ML on Hadoop → fault-tolerant training  
- **Flask**: Simple real-time UI → shows AUC, accuracy, HDFS/MongoDB stats

### License
MIT License – see [LICENSE](LICENSE) file
