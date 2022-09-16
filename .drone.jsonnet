[{
    kind: "pipeline",
    name: "lib",

    platform: {
        os: "linux",
        arch: "amd64"
    },
    steps: [
        {
            name: "version",
            image: "debian:buster-slim",
            commands: [
                "echo $DRONE_BUILD_NUMBER > version"
            ]
        },
        {
            name: "test",
            image: "python:3.8-slim-buster",
            commands: [
                "pip install -e .",
                "pip install -r requirements.txt",
                "py.test"
            ]
        },
        {
            name: "deploy",
            image: "python:3.8-slim-buster",
            environment: {
                PYPI_LOGIN: {
                    from_secret: "PYPI_LOGIN"
                },
                PYPI_PASSWORD: {
                    from_secret: "PYPI_PASSWORD"
                }
            },
            commands: [
                "./upload.sh"
            ]
        }
    ]
}]