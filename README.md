# Helm Chart Manager

Helm Chart Manager es una aplicación en Python que permite descubrir y gestionar Helm Charts desde Artifact Hub, y desplegarlos en un clúster de Kubernetes. Fue creada como parte de un desafío técnico para integrar APIs externas con herramientas de orquestación de contenedores.

## Funcionalidades

- Buscar charts en Artifact Hub por palabra clave.
- Mostrar información detallada de un chart específico.
- Agregar el repositorio Helm correspondiente si no está presente.
- Instalar o actualizar un chart en un clúster de Kubernetes.
- Listar todos los releases instalados con Helm.
- Desinstalar releases.

## Requisitos

- Python 3.8 o superior.
- Helm instalado y accesible desde la terminal.
- Un clúster de Kubernetes funcional (como Minikube).
- `kubectl` configurado para interactuar con el clúster.
- Conexión a internet para consultar Artifact Hub.

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/Alvaro-Jhair/helm-chart-manager.git
cd helm-chart-manager
