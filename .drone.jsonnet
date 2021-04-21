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
            image: "syncloud/build-deps-amd64",
            commands: [
                "echo $DRONE_BUILD_NUMBER > version"
            ]
        },
        {
            name: "test",
            image: "python:alpine3.13",
            commands: [
                "apk update && apk add py-cryptography",
                "pip install -e .",
                "pip install -r dev_requirements.txt",
                "py.test"
            ]
        },
        {
            name: "deploy",
            image: "syncloud/build-deps-amd64",
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