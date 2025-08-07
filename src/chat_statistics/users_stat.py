from src.data import DATA_DIR
from typing import Union
from pathlib import Path
from src.utils.io import read_json, read_file
from loguru import logger

#defining class for the telegram groupe
class GroupStatistics:
    """This is a classs for a telegram group info
    """    
    def __init__(self, file_path: Union[str, Path]):
        """
        Args:
            file_path (Union[str, Path]): file path of group chats
        """   
        logger.info("The initialization has been started...")     
        self.data = read_json(file_path)
        self.group_name = self.data['name']
        self.group_type = self.data['type']
        self.group_id = self.data['id']
        self.group_messages = self.data['messages'][1:]
        self.users_info = {}
        self._add_users_info()
    
    def _add_users_info(self):
        """This methods iterates in messages and create users info
        """    
        logger.info("Adding users information...")    
        for message in self.group_messages:
            if not message.get('from_id'):
               continue 
            if self.users_info.get(message['from_id']):
                self._check_message(message)
                continue
            
            self.users_info[message['from_id']] = { 'user_name': message['from'],
                                                    'send_messages': 0,
                                                  'reply_messages':0,
                                                  'send_questions':0,
                                                  'reply_questions':0}
            self._check_message(message)
        
    def _fine_text_from_message(self, message):
        """_summary_

        Args:
            message (dict): the message

        Returns:
            str: the text of the message
        """  

        if isinstance(message['text'], str):
            
            return message['text']
        elif isinstance(message['text'][-1], str):
            return message['text'][-1]
        else:
            return 'None'

    def _check_message(self, message):
        """this method check the message features and conduct related operations

        Args:
            message (dict): the message
        """        
        self.users_info[message['from_id']]['send_messages'] += 1
        
        self.users_info[message['from_id']]['send_questions'] +=\
        1 if self._is_question(message) else 0
        
        self.users_info[message['from_id']]['reply_messages'] +=\
        1 if message.get('reply_to_message_id') else 0

        self.users_info[message['from_id']]['reply_questions'] +=\
        1 if message.get('reply_to_message_id') and self._is_question(
            self._find_message_from_id(message['reply_to_message_id'])) else 0        


        
    def _find_message_from_id(self, id_):
        """this method finds the message based on the provided id

        Args:
            id_ (int): message id

        Returns:
            dict: message
        """        
        for message in self.group_messages:
            if message['id'] == id_:
                return message
        return 'Message was not found'
        

    def _is_question(self, message):
        """this method tells if a message is question or not

        Args:
            message (dict): message

        Returns:
            bool: True if the message is question and False if not
        """        
        if message == 'Message was not found':
            return False
        
        if set(self._fine_text_from_message(message)).intersection({'?','؟'}):
            return True
        else:
            return False

if __name__ == "__main__":
    Sample_obj = GroupStatistics(DATA_DIR / 'online.json')
    
    