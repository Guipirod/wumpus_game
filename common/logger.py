from os import makedirs
from os.path import join, isfile, exists


class Logger:

    def __init__(self, game_name: str, silence: bool = False):
        self._total_messages = 0
        self._silence_mode = silence  # Made so unit tests don't fill the log folder with useless data

        if not exists('logs'):
            makedirs('logs')

        if not self._silence_mode:
            for n in range(1000):
                self.file_name = f'{game_name}_{n:03}.txt'
                self.file_path = join('logs', self.file_name)
                if not isfile(self.file_path):
                    break

            else:
                raise Exception(f'You already have 1000 "{game_name}" game logs saved')

            open(self.file_path, 'w').close()

    def append_file(self, message: str):

        with open(self.file_path, 'a') as open_file:
            open_file.write(f'\n{message}')

    def log(self, message: str, player_action: bool = True):
        if not self._silence_mode:
            if player_action:
                self._total_messages += 1

            self.append_file(f'{self._total_messages} - {message}')
