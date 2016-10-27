from __future__ import print_function
import configargparse
from file_markov import FileMarkov
    
if __name__ == "__main__":
    
    p = configargparse.ArgParser(ignore_unknown_config_file_keys=True)
    p.add('-c', '--my-config', is_config_file=True, help='config file path')
    
    p.add('-f', '--file', help='File to use as a base ()')
    p.add('-e', '--encoding', default='utf8', help='Encoding for file')
    p.add('--state-size', default=1, type=int, help='State size for markov chain')
    p.add('--max-sentences', default=10, help='Number of sentences to return')
    
    options = p.parse_args()
    
    m = FileMarkov( options.file, encoding=options.encoding, state_size=options.state_size )
    for i in m.get_sentences( max_sentences=options.max_sentences ):
        print( i )