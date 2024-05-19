class Response:
    # Função lambda que retorna um dicionário
    make = lambda status=True, msg='', data=[]: {'status': status, 'msg': msg, 'data': data}
