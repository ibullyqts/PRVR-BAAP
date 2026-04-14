name: Double-Nitro Burst

on:
  workflow_dispatch:

jobs:
  burst:
    runs-on: ubuntu-latest
    strategy:
      # This runs 2 separate machines simultaneously
      matrix:
        machine_id: [1, 2] 
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install
        run: pip install instagrapi

      - name: Run Overdrive
        env:
          INSTA_COOKIE: ${{ secrets.INSTA_COOKIE }}
          TARGET_THREAD_ID: ${{ secrets.TARGET_THREAD_ID }}
          TARGET_NAME: ${{ secrets.TARGET_NAME }}
          MACHINE_ID: ${{ matrix.machine_id }} # Passes ID to the script
        run: python main.py
