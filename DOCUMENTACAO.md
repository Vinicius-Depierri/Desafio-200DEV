# **Monitoramento de Aplicações Python com Grafana, Prometheus e Tempo**  

Este projeto demonstra a implementação de um sistema de monitoramento distribuído para duas aplicações Flask (`app_a` e `app_b`), utilizando:  
- **Prometheus** para métricas.  
- **Tempo** (Grafana Tempo) para traces distribuídos.  
- **Grafana** para visualização.  
 
## **Aplicações**  
1. **`app_a`**:  
    - Flask app com endpoint `/health` (retorna status `UP`).  
    - Expõe métricas do Prometheus (`/metrics`).  
    - Gera logs em `/app/logs/app.log`.  
    - Instrumentada com OpenTelemetry para enviar traces ao Tempo.  

2. **`app_b`**:  
    - Faz chamadas HTTP para `app_a` e repassa a resposta.  
    - Também instrumentada com OpenTelemetry para traces.  

## **⚠️ Problemas Encontrados**  
1. **Grafana Loki**:  
    - Não inicializou corretamente (possível conflito de configuração ou volume).  
    - Logs de `app_a` não foram coletados.  

2. **Grafana Alloy**:  
    - Falha na inicialização (verificar `alloy-config.yaml` e permissões).  

## **🚀 Como Executar**  
1. **Suba os containers**:  
   ```bash
   docker-compose up -d

2. **Permissão**:
    - Execute este comando para dar permissão ao Grafana para escrever no diretório `/var/lib/grafana` dentro do container.
    - (NÃO RECOMENDADO PARA PRODUÇÃO)
    ```bash
    sudo chmod -R 777 grafana-storage/

3. **Acesse**:
    - Grafana: `http://localhost:3000` (usuário/senha: admin/admin).
    - Prometheus: `http://localhost:9090`.
    - app_a: `http://localhost:8080/health`.
    - app_b: `http://localhost:8081`.

    