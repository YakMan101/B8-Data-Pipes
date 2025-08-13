# B8 Data Pipes

A Dagster-based data pipeline for B8 data schediles.

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Configure environment variables** in `.env`:
   - Firebase service account credentials
   - Discord webhook URL

3. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

4. **Start Dagster**:
   ```bash
   uv run dagster dev
   ```

5. **Access the UI** at http://localhost:3000

## Environment Variables

### Firebase (Service Account)
```
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"
FIREBASE_CLIENT_EMAIL=your_service_account@project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_CLIENT_CERT_URL=https://...
```

### Discord
```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```
