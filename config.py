import os
import getpass

# misc
recommended_version = 1.1

# user details
current_user    = getpass.getuser()
centinel_home   = os.path.join(os.path.expanduser('~'+current_user),
                               '.centinel')

# directory structure
results_dir     = os.path.join(centinel_home, 'results')
experiments_dir = os.path.join(centinel_home, 'experiments')
inputs_dir = os.path.join(centinel_home, 'inputs')

# sqlite
sqlite_db       = os.path.join(centinel_home, 'db.sqlite')
maxmind_db      = os.path.join(centinel_home, 'maxmind.mmdb')

# web server
ssl_cert = "server.iclab.org.crt"
ssl_key  = "server.iclab.org.key"
