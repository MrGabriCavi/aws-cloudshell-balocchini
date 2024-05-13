#!/bin/bash

echo "Selezionando un cluster ECS..."

# Lista dei cluster, assicurandosi che ogni ARN sia su una propria riga
mapfile -t clusters < <(aws ecs list-clusters --query "clusterArns[]" --output text | tr '\t' '\n')
select cluster in "${clusters[@]}"; do
    if [ -n "$cluster" ]; then
        echo "Hai selezionato il cluster $cluster"
        break
    else
        echo "Selezione non valida. Riprova."
    fi
done

echo "Selezionando un servizio ECS nel cluster $cluster..."

# Lista dei servizi nel cluster selezionato, assicurandosi che ogni ARN sia su una propria riga
mapfile -t services < <(aws ecs list-services --cluster "$cluster" --query "serviceArns[]" --output text | tr '\t' '\n')
select service in "${services[@]}"; do
    if [ -n "$service" ]; then
        echo "Hai selezionato il servizio $service"
        break
    else
        echo "Selezione non valida. Riprova."
    fi
done

echo "Selezionando un task nel servizio $service..."

# Lista dei task nel servizio selezionato, assicurandosi che ogni ARN sia su una propria riga
mapfile -t tasks < <(aws ecs list-tasks --cluster "$cluster" --service-name "$service" --query "taskArns[]" --output text | tr '\t' '\n')
select task in "${tasks[@]}"; do
    if [ -n "$task" ]; then
        echo "Hai selezionato il task $task"
        break
    else
        echo "Selezione non valida. Riprova."
    fi
done

echo "Selezionando un container nel task $task..."

# Ottieni i dettagli del task selezionato, inclusi i nomi dei container, assicurandosi che ogni nome sia su una propria riga
mapfile -t containers < <(aws ecs describe-tasks --cluster "$cluster" --tasks "$task" --query "tasks[0].containers[].name" --output text | tr '\t' '\n')
select container in "${containers[@]}"; do
    if [ -n "$container" ]; then
        echo "Hai selezionato il container $container"
        break
    else
        echo "Selezione non valida. Riprova."
    fi
done

# Connettiti al container via SSM
echo "Connessione al container $container nel task $task..."
aws ecs execute-command \
  --cluster "$cluster" \
  --task "$task" \
  --container "$container" \
  --command "/bin/bash" \
  --interactive