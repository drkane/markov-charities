from file_markov import FileMarkov
from bottle import route, run, template
import configargparse

def main():
    
    p = configargparse.ArgParser(ignore_unknown_config_file_keys=True)
    p.add('-c', '--my-config', is_config_file=True, help='config file path')
    
    p.add('--charity-file', default='charities.csv.gz', help='Charity file to use as a base')
    p.add('--cic-file', default='cics.csv.gz', help='CIC file to use as a base')
    p.add('--host', default='localhost', help='Host for website')
    p.add('-p', '--port', default=8080, type=int, help='Port for website')
    
    options = p.parse_args()
    
    cic_m = FileMarkov(options.cic_file)
    char_m = FileMarkov(options.charity_file)

    @route('/cic/')
    def index():
        return cic_m.get_sentence()

    @route('/charity/')
    def index():
        return char_m.get_sentence()

    run(host=options.host, port=options.port)

if __name__ == "__main__":
    main()