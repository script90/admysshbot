clear

if [ ! -d "bot" ]; then
	mkdir bot
fi

cd bot

if [ -e "dadosBot.ini" ] ; then

	screen -X -S bot quit > /dev/null
	screen -dmS bot php bot.php
	echo "Bot foi reiniciado e está executano em segundo plano"

else

echo "Instalando dependencias, aguarde..."

#add-apt-repository ppa:ondrej/php > /dev/null 2>&1

apt-get update > /dev/null 2>&1
apt-get upgrade -y > /dev/null 2>&1
apt-get install php -y > /dev/null 2>&1
apt-get install php-redis -y > /dev/null 2>&1
apt-get install php-curl -y > /dev/null 2>&1
apt-get install php5 -y > /dev/null 2>&1
apt-get install php5-redis -y > /dev/null 2>&1
apt-get install php5-curl -y > /dev/null 2>&1
apt-get install redis-server -y > /dev/null 2>&1
apt-get install redis -y > /dev/null 2>&1
apt-get install screen -y > /dev/null 2>&1
apt-get install zip -y > /dev/null 2>&1

wget https://raw.githubusercontent.com/script90/admysshbot/master/gerarusuario-sshplus.sh -O gerarusuario.sh; chmod +x gerarusuario.sh > /dev/null

wget https://raw.githubusercontent.com/script90/admysshbot/master/%40admysshbot.zip -O bot.zip && unzip bot.zip > /dev/null

rm dadosBot.ini > /dev/null

clear

ip=$(wget -qO- ipv4.icanhazip.com/)

echo "Digite o toke do seu bot:"
read token
clear
echo "ip=$ip
token=$token
limite=100" >> dadosBot.ini

screen -dmS bot php bot.php

rm bot.zip

echo "Pronto, o bot esta executando em segundo plano
Agradeça a @Script90 ©"

fi
