cd ~/.ssh
cp id_rsa id_rsa_backup
cp id_rsa.pub id_rsa_backup.pub
ssh-keygen -t rsa -C "mikemiles19@gmail.com"
