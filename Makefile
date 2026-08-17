PYTHON = python3
PIP = pip

all: install collect preprocess topics network

install:
	@echo "📦 Installing project dependencies..."
	$(PIP) install -r requirements.txt

collect:
	@echo "📡 [1/4] Collecting posts from the Bluesky API..."
	$(PYTHON) src/collect_posts.py

preprocess:
	@echo "🧹 [2/4] Preprocessing textual data..."
	$(PYTHON) src/preprocess_text.py

topics:
	@echo "🎯 [3/4] Running TF-IDF and LDA topic modeling..."
	$(PYTHON) src/topic_modeling.py

network:
	@echo "🕸️ [4/4] Building the co-occurrence network and detecting communities..."
	$(PYTHON) src/network_analysis.py

rank-users:
	@echo "👥 Ranking high-engagement users within detected communities..."
	$(PYTHON) src/rank_community_users.py

timelines:
	@echo "🗂️ Collecting recent posts from selected community users..."
	$(PYTHON) src/collect_user_timelines.py

clean:
	@echo "🧽 Removing generated datasets and plots..."
	rm -f *.csv
	rm -f *.png

.PHONY: all install collect preprocess topics network rank-users timelines clean
