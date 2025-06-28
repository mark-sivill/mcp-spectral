# mcp-spectral

Model Context Protocol (MCP) Server for Spectral to lint OpenAPI specifications

## Overview

The goal of this project is to reduce hallucinations within [Large Language Models](https://en.wikipedia.org/wiki/Large_language_model) (LLM) by allowing the LLM to automatically check with third-party tools that the work it has created is "correct", and optionally allow the LLM to update it's work until it is more "correct". 

The third-party tool in this case is [Spectral](https://stoplight.io/open-source/spectral) which lints/validates [OpenAPI Specifications](https://swagger.io/specification/). The LLM is asked to generate an OpenAPI specification which may or may not contain halluncinations, the generated OpenAPI specification is checked against Spectral to see if there any lint/validation errors automatically by the LLM, if Spectral reports any problems the LLM can act on them to create an updated OpenAPI specification, which can be checked again with Spectral. These last steps are repeated until a more "correct" OpenAPI specification is created.

The worked example will allow API developers to generate OpenAPI specifications quicker against existing APIs that do not have an OpenAPI specification defined, so speeding up API delivery times. Conceptually it also shows a pattern to reduce hallucinations within Artificial Intelligence (AI) tools.

## Set up instructions

The following instructions set up a [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) (MCP) Server that lints/validates an OpenAPI specification using [Spectral](https://stoplight.io/open-source/spectral) in a [Docker](https://www.docker.com/) container which is then used by the [Anthropic](https://www.anthropic.com/) [Claude Desktop](https://claude.ai/download)

### Install

Ensure the following applications are installed on the local machine

[Claude Desktop install](https://claude.ai/download)
[Docker install](https://docs.docker.com/engine/install/)

### Update Claude Desktop

Add following to the [claude_desktop_config.json ](https://modelcontextprotocol.io/quickstart/user) file within the Claude Desktop installation

```
"OpenAPI linting (Spectral)": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "marksivill/mcp-spectral"
      ]
    }
```

