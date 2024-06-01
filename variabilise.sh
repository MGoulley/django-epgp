set -x

DB_HOST="$1"
DB_PORT="$2"
DB_USER="$3"
DB_PASSWORD="$4"
DB_NAME="$5"
FILE="$6"

sed -i -e "/database =/s/=.*/= \"$DB_NAME\"/" $FILE
sed -i -e "/user =/s/=.*/= \"$DB_USER\"/" $FILE
sed -i -e "/password =/s/=.*/= \"$DB_PASSWORD\"/" $FILE
sed -i -e "/host =/s/=.*/= \"$DB_HOST\"/" $FILE
sed -i -e "/port =/s/=.*/= \"$DB_PORT\"/" $FILE
