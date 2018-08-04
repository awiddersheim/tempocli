import yaml


def write_yaml(config, data):
    config.write(
        yaml.safe_dump(
            data,
            default_flow_style=False,
            explicit_start=True,
        ),
    )
