def translate_arinc429_message(msg):
    label = msg.label
    data = msg.data
    ssm = msg.ssm

    label_map = {
        101: f"GPS Position: {data} meters",
        202: f"FMS Waypoint: {data}",
        303: f"EFIS Altitude: {data} ft",
        404: f"Autopilot Mode: {data}",
        505: f"Air Speed: {data} knots",
        606: f"Vertical Speed: {data} ft/min",
        707: f"Heading: {data}°",
        808: f"Engine Temp: {data}°C",
        909: f"Fuel Flow: {data} kg/h",
        999: "FAULT INJECTION DETECTED"
    }

    status_map = {
        0: "Failure Warning",
        1: "Functional Test",
        2: "Not Computed",
        3: "Normal Operation"
    }

    label_text = label_map.get(label, f"Label {label}: Data {data}")
    ssm_text = status_map.get(ssm, f"SSM {ssm}")

    return f"{label_text} | Status: {ssm_text}"
