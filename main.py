#!/usr/bin/python3
import discord
import mctools
import re
from config import *

# Define classes
class RCONHandler():
    def __init__(self, rcon_host, rcon_password, rcon_port):
        self.rcon_host = rcon_host
        self.rcon_password = rcon_password
        self.rcon_port = rcon_port
        self._initialize_rcon()

    def send_command(self, command):
        try:
          response = self._format_output(self.rcon_client.command(command))

        # if "Connection timeout error" exception, reconnect and try again
        except:
            self._initialize_rcon()
            response = self._format_output(self.rcon_client.command(command))

        # If response is an empty string, return a more descriptive message
        if response == '':
            return 'Command returned no output.'
        else:
            return response

    def disconnect(self):
        self.rcon_client.disconnect()

    def _initialize_rcon(self):
        self.rcon_client = mctools.RCONClient(self.rcon_host, port=self.rcon_port)
        self.rcon_client.login(self.rcon_password)

        # if login fails, print exception. Else, print login message
        if self.rcon_client.is_authenticated():
            print('RCON connection established.')
        else:
            print('RCON connection failed.')

    def _format_output(self, line):
        ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', line)

class DiscordHandler(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rcon_handler = RCONHandler(RCON_HOST, RCON_PASSWORD, RCON_PORT)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # Ignore messages from self
        if message.author == self.user:
            return

        # Ignore messages from other channels
        if message.channel.id != CHANNEL_ID:
            return

        # Ignore messages that don't start with the prefix
        if not message.content.startswith('/'):
            return

        # Print status to console, execute command, and send response to discord
        print(f'{message.author.name} said: {message.content}')
        response = self.rcon_handler.send_command(message.content[1:])
        await message.channel.send(response)
        print(f'Response: {response}')
        print('------')

def main():
    print('Starting Discord client...')
    discord_handler = DiscordHandler()
    discord_handler.run(DISCORD_TOKEN)

if __name__ == main():
    main()
    print("Disconnected from server")
    print("Exiting...")
    exit()