# Local Instance Instructions

1) Open Visual Studio Code
2) Open a new terminal, and clone this GitHub repository using the following command. When prompted, open the clone repository folder:
```powershell
git clone https://github.com/Cyber-Tutor/Cyber-Tutor-Firestore-Data-Dumping.git
```
3) Create and activate a Python virtual environment using the following commands:
```powershell
python -m venv .venv
.venv\Scripts\activate
```
4) Install packages from requirements.txt using the following command:
```powershell
pip install -r requirements.txt
```
5) Get the serviceAccountKey.json from Firestore, or our GitHub wiki
6) The applicable commands are:
```bash
python download_collection_quizQuestions.py
python download_collection_topics.py
python upload_collect_demographicSurveyQuestions.py
pytohn upload_collect_initialSurveyQuestions.py
python upload_collection_quizQuestions.oy
python upload_collection_topics.py```