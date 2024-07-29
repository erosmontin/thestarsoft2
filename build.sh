git clone https://${token}@github.com/EliMarchetto/OAI_DataProcessing.git

docker build  -t erosmontin/thestarsoft2:latest .

rm -rf OAI_DataProcessing


#docker tag t2julia:latest erosmontin/thestarsoft2:latest


docker push erosmontin/thestarsoft2:latest