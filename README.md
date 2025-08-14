# B8 Data Pipes

A Dagster-based data pipeline for generating weekly booking reports from Firebase and sending them to Discord.

## Prerequisites

- Python 3.12+
- Firebase project with service account credentials
- Discord webhook URL

## Setup

1. **Create and activate virtual environment**:

   **Linux/macOS**:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

   **Windows**:
   ```cmd
   python3.12 -m venv venv
   venv\Scripts\activate
   ```

2. **Install uv package manager**:
   ```bash
   pip install uv
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Fill in your Firebase service account credentials
   - Add your Discord webhook URL

5. **Start Dagster development server**:
   ```bash
   uv run dagster dev
   ```

6. **Access the UI** at http://localhost:3000

## Environment Variables

Create a `.env` file based on `.env.example` with your actual credentials:

- **Firebase**: Service account credentials from your Firebase project
- **Discord**: Webhook URL for sending reports
- **USE_EMULATORS**: Set to `true` for local Firebase emulator development
