TAG=1.0.0
IMAGE_NAME=datasync-event-handler
ACCOUNT_URI=353276416433.dkr.ecr.us-east-1.amazonaws.com
REPO_URI=$ACCOUNT_URI/$IMAGE_NAME
IMAGE_URI=$REPO_URI:$TAG

docker build . -t $IMAGE_NAME
docker tag $IMAGE_NAME $IMAGE_URI
aws ecr get-login-password --region us-east-1 --profile=gsat | docker login --username AWS --password-stdin $ACCOUNT_URI
docker push $IMAGE_URI
aws lambda  update-function-code --function-name $IMAGE_NAME --image-uri $IMAGE_URI --publish --profile=gsat --region=us-east-1
