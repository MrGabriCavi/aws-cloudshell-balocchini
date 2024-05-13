#!/bin/bash

profile_arg="--profile $1"

echo "Elenco delle istanze EC2 raggiungibili tramite SSM:"

# Ottieni l'elenco degli ID delle istanze gestite da SSM utilizzando le credenziali di default o la configurazione ambientale
instance_ids=$(aws $profile_arg ssm describe-instance-information --query 'InstanceInformationList[].InstanceId' --output text)

declare -a instance_array=()
index=1

# Itera sugli ID delle istanze e ottieni i nomi delle istanze utilizzando le credenziali di default o la configurazione ambientale
for id in $instance_ids; do
    name=$(aws $profile_arg ec2 describe-tags --filters "Name=resource-id,Values=$id" "Name=key,Values=Name" --query 'Tags[?Key==`Name`].Value' --output text)
    # Controlla se il nome è vuoto, che indica che il tag Name non è stato trovato
    if [ -z "$name" ]; then
        name="No Name Tag"
    fi
    echo "$index) $id ($name)"
    instance_array[$index]=$id
    let index+=1
done

# Chiedi all'utente di scegliere un'istanza
echo "Inserisci il numero dell'istanza per avviare una sessione SSM (lascia vuoto per uscire):"
read selection

# Verifica se la selezione è un numero entro l'intervallo valido
re='^[0-9]+$'
if ! [[ $selection =~ $re ]] ; then
   echo "Uscita: selezione non valida"
   exit 1
fi

if [ $selection -le 0 ] || [ $selection -ge $index ]; then
    echo "Uscita: selezione fuori dall'intervallo valido"
    exit 1
fi

# Avvia una sessione SSM con l'istanza selezionata
selected_instance=${instance_array[$selection]}
echo "Avvio sessione SSM con l'istanza: $selected_instance"
aws $profile_arg ssm start-session --target $selected_instance
