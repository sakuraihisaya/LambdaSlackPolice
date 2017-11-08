# -*- coding: utf-8 -*-
import os
import time

from slacker import Slacker


class SlackPolice(object):
    
    def __init__(self, token=None):
        token = os.environ.get('SLACK_API_TOKEN', token)
        self.__slacker = Slacker(token)

    def get_file_list(self):
        """
        Fetch files in the slack team.
        """
        raw_data = self.__slacker.files.list().body
        
        return raw_data['files']
        
    def delete_file(self, file_id):
        """
        Delete specified file.
        """
        response = self.__slacker.files.delete(file_id).body

        return response

    def delete_all_files(self):
        """
        Delete all files in the slack team.
        """
        channel_set = set()
        files = self.get_file_list()
        for file in files:
            if file['filetype'] == 'text':  # without code snippet
                continue
            res = self.delete_file(file['id'])
            channel_set.update(file['channels'])#重複しない

            if 'ok' in res and res['ok']:
                print('{0} deleted.'.format(file['name']))
            else:
                print("{0} could not be deleted.".format(file['name']))

        message = '月次点検のため、ファイルを削除しました。'
        self.post_message_to_channels(channel_set, message)

    def post_message_to_channels(self, channels, message):
        """
        Post message to arbitrary channel in the team.
        """
        for channel in channels:
            self.__slacker.chat.post_message(channel, message, username='', icon_url='')

def slackpolice(event, context):
    police = SlackPolice()
    police.delete_all_files()
