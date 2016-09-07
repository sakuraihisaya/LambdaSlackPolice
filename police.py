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
        files = self.get_file_list()
        for file in files:
            res = self.delete_file(file['id'])
            if 'ok' in res and res['ok']:
                print('{0} deleted.'.format(file['name']))
                message = 'ファイルは削除しました。ファイルアップロードは禁止ですよ。'
                self.post_message_to_channels(file['channels'], message)
            else:
                print("{0} could not be deleted.".format(file_name))

    def post_message_to_channels(self, channels, message):
        """
        Post message to arbitrary channel in the team.
        """
        for channel in channels:
            self.__slacker.chat.post_message(channel, message, username='', icon_url='')


if __name__ == '__main__':
    interval_sec = 10
    police = SlackPolice()
    while True:
        police.delete_all_files()
        time.sleep(interval_sec)
