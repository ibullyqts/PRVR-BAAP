name: Phoenix V100 Hybrid Cluster (6-Hour)

on:
  workflow_dispatch:
  schedule:
    # Runs every 6 hours sharp (00:00, 06:00, 12:00, 18:00 UTC)
    - cron: "0 */6 * * *"

env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true 

jobs:
  launch:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        # Running 5 machines every 6 hours = 20 strikes per day
        machine-id: [1, 2, 3, 4, 5 ,6 ,7 ,8 ,9, 10, 11, 12]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install
        run: |
          pip install playwright
          playwright install chromium
      - name: Run
        env:
          INSTA_COOKIE: ${{ secrets.INSTA_COOKIE }}
          TARGET_THREAD_ID: ${{ secrets.TARGET_THREAD_ID }}
          TARGET_NAME: ${{ secrets.TARGET_NAME }}
        run: python -u main.py
