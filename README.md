# CTF Buddy

CTF Buddy is a simple Discord bot that helps users find and organize teams for CTFs. The bot allows a user to react to a message and randomly assigns them into a team.

## Commands

### `!ctf_lfg <CTF_NAME>`
Starts a new LFG request.

The bot will send a message:
 ```React with ✅ if you are looking for a team for HackTheBox! ```

Users then react to the message to participate.

### `!ctf_team TS=<TEAM_SIZE>`
Creates random teams with the specified team size from users who reacted.

**Example:**
!ctf_team TS=4


The bot will then respond with:

**CTF Teams for HackTheBox:**

- **Team 1:** @user1 @user2 @user3 @user4
- **Team 2:** @user5 @user6 @user7 @user8

### `!ctf_help`
Displays a help message explaining commands.


## Setup Instructions

### Prerequisites:
- Python 3.9+
- Docker (optional, for containerized deployment)
- A Discord bot token

### Python Setup:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/CTF_Buddy.git
    cd CTF_Buddy
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file and add your bot token:
    ```env
    DISCORD_BOT_TOKEN=insert_bot_token_here
    ```

4. Run the bot:
    ```bash
    python ctf_Buddy.py
    ```

### Docker Deployment:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/CTF_Buddy.git
    cd CTF_Buddy
    ```

2. Build the Docker image:
    ```bash
    docker build -t ctf-buddy .
    ```

3. Run the container:
    ```bash
    docker run --name ctf-buddy ctf-buddy
    ```
