import boto.sns

conn = boto.sns.connect_to_region('us-west-2')

res = conn.subscribe('arn:aws:sns:us-west-2:503791085592:twitter',
                'http', 'http://twittmap-dev.us-west-2.elasticbeanstalk.com/')

print res
