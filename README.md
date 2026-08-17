# Bluesky Community Analysis

End-to-end data mining, text mining and social network analysis project applied to public posts from the **Bluesky** social network, using the Pokémon fandom as a case study.

The project was developed for the **Social Network Mining and Analysis** course at the Federal University of São João del-Rei (UFSJ).

Rather than focusing on a single algorithm, the work evolved through several stages of the course, including:

* exploratory data analysis;
* behavioral clustering;
* natural language processing;
* topic modeling;
* graph construction;
* community detection;
* qualitative analysis of high-engagement users.

The main goal was to investigate whether different computational methods could reveal meaningful behavioral and thematic structures inside the Pokémon community on Bluesky.

---

## Project Overview

The project was developed incrementally across multiple course assignments.

The analyses can be organized into three main stages:

```text
Bluesky API
    |
    v
Data Collection
    |
    +----------------------+
    |                      |
    v                      v
User-level features     Raw post text
    |                      |
    v                      v
EDA + Min-Max          Text preprocessing
    |                      |
    v                      v
K-Means + PCA          TF-IDF + LDA
                           |
                           v
                  Co-occurrence network
                           |
                           v
                 Louvain communities
                           |
                           v
              High-engagement user analysis
                           |
                           v
                  Timeline inspection
```

The earlier stages focused on **user behavior**, while later stages shifted toward **semantic structure and network topology**.

---

## Research Questions

The project explored questions such as:

* Can Bluesky users discussing the same broad topic be separated into distinct behavioral profiles?
* Do engagement, media usage, hashtags and text length reveal meaningful user groups?
* Which latent topics emerge from posts with different levels of engagement?
* Can a co-occurrence network of terms reveal coherent thematic communities?
* Do communities detected topologically correspond to the topics identified through text mining?
* Are highly engaged users within a thematic community focused primarily on Pokémon, or do they participate in broader discussions?

---

# 1. Data Collection

Data was collected directly from the Bluesky API.

The main text-mining pipeline collected approximately **1,000 public posts containing the keyword `Pokémon`**.

The final collector used raw HTTP requests with the `requests` library instead of relying exclusively on a high-level client.

This approach allowed the pipeline to:

* access Bluesky XRPC endpoints directly;
* process JSON responses manually;
* paginate through search results;
* recover from expired authentication tokens;
* handle rate-limit responses;
* discard malformed or empty records without interrupting the full collection process.

The collected fields included:

```text
post_id
created_at
user_handle
raw_text
like_count
```

An earlier stage of the project also aggregated posts by unique user and generated continuous behavioral attributes.

---

# 2. Behavioral Data Mining

The first major analytical stage focused on identifying behavioral profiles among users.

## User Features

Posts were aggregated by user and represented through five numerical attributes:

| Feature               | Description                             |
| --------------------- | --------------------------------------- |
| `frequencia_posts`    | Number of collected posts from the user |
| `engajamento_medio`   | Average number of likes per post        |
| `tamanho_medio_texto` | Average post length                     |
| `taxa_midia`          | Proportion of posts containing media    |
| `uso_medio_hashtags`  | Average number of hashtags per post     |

The resulting dataset contained **743 users** in the reported experiment.

---

## Exploratory Data Analysis

Before clustering, the project performed:

* descriptive statistics;
* histogram analysis;
* boxplot analysis;
* Pearson correlation analysis;
* missing-value and infinite-value removal;
* Min-Max normalization.

The exploratory analysis revealed strong engagement outliers, suggesting that a relatively small number of users captured a large fraction of the observed attention.

One of the clearest correlations appeared between:

```text
media usage ↔ hashtag usage
```

with a reported Pearson correlation of approximately:

```text
r = 0.31
```

This was interpreted as evidence that visually oriented accounts — such as artists or image-sharing profiles — often relied more heavily on hashtags for visibility.

---

## K-Means Clustering

Behavioral profiles were explored using **K-Means**.

Candidate values were evaluated in the range:

```text
K = 2 ... 10
```

using the **Calinski-Harabasz Index**.

The highest numerical score occurred at:

```text
K = 2
```

However, the alternative:

```text
K = 4
```

also obtained a competitive score and resulted in more interpretable behavioral subgroups.

---

## PCA Visualization

Since the clustering used five numerical dimensions, **Principal Component Analysis (PCA)** was used to project users into two dimensions for visualization.

The `K = 4` configuration produced four interpretable behavioral profiles.

### Casual Short-Text Users

Users with:

* short posts;
* low media usage;
* low engagement.

Reported average engagement:

```text
~1.60 likes
```

### Discussion-Oriented Users

Users characterized by:

* longer posts;
* low media usage;
* stronger participation in discussions.

Reported average engagement:

```text
~2.58 likes
```

### Artists and Promoters

Profiles characterized by:

* frequent image usage;
* higher hashtag usage;
* portfolio-oriented content.

Reported average engagement:

```text
~5.25 likes
```

### Meme and Short-Form Media Accounts

Profiles characterized by:

* high media usage;
* very short text;
* memes or short-form informational content.

This group achieved the highest reported engagement:

```text
~6.48 likes
```

The complete cluster characterization is documented in the original KDD report.

---

# 3. Text Preprocessing

A second branch of the project focused directly on post content.

The NLP preprocessing pipeline included:

```text
Raw text
   |
   v
URL removal
   |
   v
Mention removal
   |
   v
Special-character cleanup
   |
   v
Lowercasing
   |
   v
Tokenization
   |
   v
Portuguese + English stopword removal
   |
   v
Snowball stemming
```

The implementation used:

* regular expressions;
* NLTK tokenization;
* Portuguese stopwords;
* English stopwords;
* Snowball Stemmer.

The project intentionally combined Portuguese and English preprocessing because the keyword `Pokémon` retrieved a multilingual corpus.

In the consolidated run, **982 valid posts** remained after preprocessing and removal of semantically empty documents.

---

# 4. Topic Modeling

The processed corpus was transformed using **TF-IDF**.

Configuration:

```text
max_features = 1000
min_df = 2
max_df = 0.95
```

Posts were then divided according to engagement using the **70th percentile of like counts**.

Topic modeling was applied separately to higher- and lower-engagement posts using **Latent Dirichlet Allocation (LDA)** with:

```text
3 latent topics
15 iterations
```

---

## High-Engagement Topics

In the consolidated experiment, the high-engagement subset contained **295 posts**.

The extracted topics were interpreted as:

### Account Management and Updates

Dominant terms included stems related to:

```text
account
run
qtp
fire
episode
```

These were associated with recurring updates and automated or semi-automated accounts.

### Games and New Releases

Terms included:

```text
game
art
get
tcg
new
```

indicating discussions around games, releases and commercial announcements.

### Engagement and Digital Art

Terms such as:

```text
like
one
nsfw
game
pokemonart
```

were associated with artists and engagement-oriented content.

---

## Low-Engagement Topics

The low-engagement subset contained **689 posts**.

The three main topics were interpreted as:

### Trading Card Game

Dominant vocabulary:

```text
sale
tcg
seal
new
box
```

### Organic Opinions and Preferences

Dominant vocabulary:

```text
like
play
game
one
pokopia
```

### Anime and Episodic Media Consumption

Dominant vocabulary:

```text
fire
frame
episode
season
timestamp
```

The topic analysis suggested that users with different levels of engagement participated in noticeably different forms of discourse.

---

# 5. Co-occurrence Network

The processed text was also modeled as a graph.

The network used:

```text
Node = dominant word stem

Edge = two stems appearing in the same post

Edge weight = number of posts in which both terms co-occur
```

The graph was built from the valid processed corpus.

Only the most frequent terms were retained, and weak co-occurrences were filtered.

This produced a compact semantic network designed to reveal broader structural relationships between recurring discussion themes.

---

# 6. Community Detection with Louvain

The **Louvain algorithm** was applied to the weighted co-occurrence graph.

In the consolidated analysis, the network achieved a modularity score of:

```text
Q = 0.5728
```

The result indicated a non-random community structure with meaningful separation between thematic groups.

Four main communities were identified.

---

## Community 1 — Media and Animation

This group concentrated vocabulary related to:

* episodes;
* seasons;
* frames;
* timestamps;
* anime discussion.

It strongly resembled the animation-oriented latent topic previously identified through LDA.

---

## Community 2 — Trading Card Game

This community contained terms associated with:

* TCG products;
* cards;
* booster packs;
* boxes;
* sales;
* collecting.

It also closely matched a topic previously identified by LDA.

---

## Community 3 — Engagement Mechanics

The third group captured vocabulary associated with:

* automated accounts;
* interactive posts;
* engagement prompts;
* quote-based viral mechanics.

Terms such as `qtp` helped distinguish this group.

---

## Community 4 — General Interaction and Art

The final community included broader fan interaction together with:

* fanart;
* general gaming vocabulary;
* conversational terms;
* digital illustration.

---

## Network Visualization

The original analysis generated a spring-layout visualization of the term network, with node colors representing Louvain communities and node sizes reflecting graph degree.

A version of this visualization is included in the technical report located in:

```text
docs/final-report.pdf
```

The graph visually shows the separation between the TCG vocabulary, animation-related terms, engagement mechanics and broader art/general interaction cluster.

---

# 7. Cross-Method Comparison

One of the most interesting findings was the consistency between the independently generated results.

The **LDA topic model** and the **Louvain graph communities** both identified structures related to:

```text
Trading Card Game
Anime / episodic media
Art and creative content
Community engagement
```

The consolidated report therefore concluded that the thematic organization discovered through text mining was also reflected in the topology of the term co-occurrence network.

This cross-method agreement was one of the central findings of the project.

---

# 8. Follow-up User Timeline Analysis

A later stage extended the graph analysis beyond vocabulary structure.

Users with high accumulated engagement inside the detected communities were selected and their recent general timelines were collected.

Rather than considering only posts containing the keyword `Pokémon`, this stage retrieved broader recent activity from those accounts.

The goal was to evaluate whether users associated with Pokémon-related communities were:

```text
primarily Pokémon-focused
```

or

```text
multithematic users who occasionally discussed Pokémon
```

The follow-up analysis examined **270 recent posts from 18 users**.

---

## Timeline Findings

The proportion of Pokémon-related content varied considerably between detected communities.

| Community                         | Pokémon-related content |
| --------------------------------- | ----------------------: |
| Engagement and Fan Interaction    |                    6.7% |
| General Discussion, Games and Art |                   37.8% |
| Media and Animation               |                   53.3% |
| TCG and Commercial                |                   45.3% |

Some profiles were almost entirely dedicated to Pokémon, while others had been associated with Pokémon-related communities because of a small number of highly visible posts.

This highlighted an important limitation of keyword-based and lexical community analysis.

Users may become structurally associated with a topic even when that topic represents only a small portion of their broader activity.

---

# 9. Methodological Limitations

The project revealed several limitations.

## API Constraints

The scope of the public API limited access to some potentially useful variables, such as:

* complete follower relationships;
* account age;
* broader profile metadata;
* full interaction histories.

These limitations prevented some variables from being incorporated into the numerical clustering stage.

---

## Keyword Sampling

The initial corpus was built around posts containing:

```text
Pokémon
```

This naturally introduces a keyword-selection bias.

The dataset therefore represents activity surrounding the query rather than the entire Bluesky social graph.

---

## Co-occurrence Network

The graph represents **term co-occurrence**, not direct user-to-user relationships.

This distinction is important.

The detected communities therefore represent **semantic structures in the corpus**, not necessarily social communities formed by follower or reply relationships.

---

## Lexical Ambiguity

Generic terms such as:

```text
game
art
like
new
```

may connect content that is lexically similar but thematically different.

The later timeline analysis showed that users assigned to the same semantic community could still differ substantially in their broader interests.

---

# 10. Repository Structure

```text
bluesky-community-analysis/
│
├── src/
│   ├── collect_posts.py
│   ├── preprocess_text.py
│   ├── topic_modeling.py
│   ├── network_analysis.py
│   ├── rank_community_users.py
│   └── collect_user_timelines.py
│
├── experiments/
│   ├── exploratory_analysis.py
│   └── kmeans_clustering.py
│
├── docs/
│   └── final-report.pdf
│
├── Makefile
├── requirements.txt
├── .gitignore
└── README.md
```

---

## `src/`

Contains the main text-mining and network-analysis pipeline.

### `collect_posts.py`

Authenticates with Bluesky and collects posts through the public API.

Implements:

* pagination;
* authentication;
* token renewal;
* rate-limit handling;
* CSV export.

### `preprocess_text.py`

Executes the NLP preprocessing pipeline:

* regex cleanup;
* lowercasing;
* tokenization;
* stopword removal;
* stemming.

### `topic_modeling.py`

Executes:

* engagement-based document splitting;
* TF-IDF vectorization;
* LDA topic modeling;
* topic visualization.

### `network_analysis.py`

Builds the weighted term co-occurrence network and applies:

* NetworkX graph modeling;
* Louvain community detection;
* modularity calculation;
* graph visualization.

### `rank_community_users.py`

Ranks users associated with detected semantic communities according to accumulated engagement.

### `collect_user_timelines.py`

Collects recent general posts from selected users for follow-up qualitative analysis.

---

## `experiments/`

Contains analyses developed during earlier stages of the course.

### `exploratory_analysis.py`

Includes:

* descriptive statistics;
* histograms;
* boxplots;
* correlation matrix;
* Min-Max normalization.

### `kmeans_clustering.py`

Includes:

* K-Means clustering;
* Calinski-Harabasz evaluation;
* PCA dimensionality reduction;
* cluster visualization.

These scripts are preserved separately because they represent an earlier behavioral-analysis branch rather than the final text/network pipeline.

---

# 11. Technologies

## Language

```text
Python
```

## Data Processing

```text
Pandas
NumPy
```

## Machine Learning

```text
Scikit-learn
K-Means
PCA
TF-IDF
Latent Dirichlet Allocation
Calinski-Harabasz Index
```

## Natural Language Processing

```text
NLTK
Regular Expressions
Snowball Stemmer
```

## Network Analysis

```text
NetworkX
python-louvain
Louvain Community Detection
```

## Visualization

```text
Matplotlib
Seaborn
```

## Data Collection

```text
Bluesky XRPC API
HTTP
Requests
JSON
```

---

# 12. Installation

Clone the repository:

```bash
git clone https://github.com/viniciusgrassis/bluesky-community-analysis.git
cd bluesky-community-analysis
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

# 13. Bluesky Credentials

The data-collection scripts require Bluesky credentials.

Create a `.env` file in the repository root:

```text
BSKY_USER=your_handle
BSKY_PW=your_password
```

The `.env` file is ignored by Git and should never be committed.

---

# 14. Running the Pipeline

The Makefile provides shortcuts for the main execution stages.

## Full Main Pipeline

```bash
make all
```

This runs:

```text
dependency installation
        ↓
post collection
        ↓
text preprocessing
        ↓
topic modeling
        ↓
network analysis
```

---

## Individual Stages

Collect data:

```bash
make collect
```

Preprocess text:

```bash
make preprocess
```

Run TF-IDF and LDA:

```bash
make topics
```

Build the network and detect communities:

```bash
make network
```

Rank high-engagement users:

```bash
make rank-users
```

Collect their recent timelines:

```bash
make timelines
```

---

# 15. Generated Files

The pipeline generates intermediate datasets and visualizations such as:

```text
dataset_pokemon_texto_bruto.csv
dataset_pokemon_texto_processado.csv
topicos_lda_*.png
comunidades_topologicas_rede.png
```

Generated CSV and PNG files are ignored by default through `.gitignore`.

This keeps the repository focused on source code while avoiding publication of unnecessary raw social-media data.

---

# 16. Earlier Experiments vs. Final Pipeline

Because the project evolved across several course assignments, the repository intentionally separates two branches.

### Earlier Behavioral Experiments

```text
experiments/
```

focuses on:

```text
user-level numerical features
→ exploratory analysis
→ Min-Max scaling
→ K-Means
→ PCA
```

### Main Text and Network Pipeline

```text
src/
```

focuses on:

```text
raw posts
→ NLP
→ TF-IDF
→ LDA
→ co-occurrence graph
→ Louvain
→ user timeline analysis
```

The results reported in different course stages were produced at different points in the project and may therefore contain slightly different sample sizes.

For that reason, this README primarily uses the **consolidated report** for the main pipeline and treats earlier reports as separate experimental stages.

---

# 17. Academic Context

This project was developed for the **Social Network Mining and Analysis** course in the Computer Science undergraduate program at:

**Federal University of São João del-Rei — UFSJ**

The work was developed progressively through multiple assignments covering:

* Knowledge Discovery in Databases;
* exploratory data analysis;
* clustering;
* text mining;
* topic modeling;
* graph modeling;
* social network analysis;
* community detection.

The consolidated report integrates these stages into a single analysis of the Pokémon ecosystem on Bluesky.

---

# 18. Main Takeaway

The project found that the Pokémon ecosystem on Bluesky is not organized around a single homogeneous fandom.

Instead, multiple computational methods independently revealed recurring substructures related to:

* animation and episodic media;
* Trading Card Game discussions and commerce;
* digital art;
* general fan interaction;
* viral engagement mechanics.

Text mining and graph-based community detection produced notably similar thematic structures.

At the same time, the later timeline analysis showed that users associated with these communities were often **multithematic**, demonstrating the difference between:

```text
the semantic structure of topic-specific posts
```

and

```text
the broader identity and behavior of the users producing them.
```

This distinction became one of the most important conclusions of the project.
