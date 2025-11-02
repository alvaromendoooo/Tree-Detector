alert_controller = False
def alertDetector(current_count, alerta_umbral):
    global alert_controller

    if (current_count >= alerta_umbral) and not alert_controller:
        print(f"ALERTA: Se detectaron {current_count} árboles !")
        alert_controller = True

    elif current_count < alerta_umbral:
        alert_controller = False

    return alert_controller        
