# MCP Spectral

Model Context Protocol (MCP) Server for Spectral to lint OpenAPI specifications

## Overview

Allow [Large Language Models](https://en.wikipedia.org/wiki/Large_language_model) (LLM) to check whether an [OpenAPI Specifications](https://swagger.io/specification/) is valid using a [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) (MCP) Server.

The MCP Spectral Server wrappers the [Spectral](https://stoplight.io/open-source/spectral) command line within a [Docker](https://www.docker.com/) image.

Using an OpenAPI specification to describe an API provides consistency across APIs, the ability to document the API, a contract on how to use the API, the ability to generate code stubs to consume and produce APIs, and API versioning. These features enable quicker API development, quicker uptake of API services, and a reduction in API maintenance.

Using MCP Spectral should reduce API development time further by helping with the OpenAPI specification phase.

### Available tools

Tools provided by MCP Spectral

* lint_openapi - lints OpenAPI specification
* lint_openapi_with_ruleset - lints OpenAPI specification with Spectral ruleset
* spectral_version - returns version of Spectral being used

## Set up instructions

These instruction assume [Anthropic](https://www.anthropic.com/) [Claude Desktop](https://claude.ai/download) will interact with the MCP Spectral server. If another Large Language Model tool is being used change the set up instructions accordlingly.

### Installation prerequisites

Ensure the following applications are installed on the local machine

* [Claude Desktop install](https://claude.ai/download)
* [Docker install](https://docs.docker.com/engine/install/)

### Update Claude Desktop

Add following to the [claude_desktop_config.json](https://modelcontextprotocol.io/quickstart/user) file within the Claude Desktop installation which tells Claude Desktop how to access MCP Spectral

```
{
  "mcpServers": {
    "OpenAPI linting (Spectral)": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "marksivill/mcp-spectral"
      ]
    }
  }
}
```

For example if MCP Spectral is also installed with [mcp/fetch](https://hub.docker.com/r/mcp/fetch) the complete claude_desktop_config.json would be

```
{
  "mcpServers": {
    "fetch": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "mcp/fetch"
      ]
    },
    "OpenAPI linting (Spectral)": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "marksivill/mcp-spectral"
      ]
    }
  }
}
```

Once the file has been updated, restart the Claude Desktop.

Claude Desktop will automatically pull the [latest docker version of MCP Spectral](https://hub.docker.com/r/marksivill/mcp-spectral) from [Docker Hub](https://hub.docker.com/)

### Local builds

Optionally the docker image can be built locally instead of pulling from Docker Hub using

```
docker build --tag marksivill/mcp-spectral:latest .
```

This is useful if the source code or default ruleset needs to be changed for example

## Example Claude Desktop prompts

Below are example prompts for Claude Desktop which may also work in other Large Language Model (LLM) tools that are calling MCP Spectral.

Note [mcp/fetch](https://hub.docker.com/r/mcp/fetch) may also need to be installed into Claude Desktop to fetch URLs.

Prompt 1

```
What version of Spectral do we have access to
```

Prompt 2

```
Validate the OpenAPI specification from OpenWeatherMap API.
If any errors are found, fix them, then revalidate, repeat the last steps until the OpenAPI specification is valid.
```

Prompt 3

```
Using the API documentation found at https://wheretheiss.at/w/developer build an OpenAPI specification.
Ensure that there are no validation errors.
If any errors are found, fix them, then revalidate, repeat the last steps until the OpenAPI specification is valid.
```

Prompt 4

```
Build an OpenAPI specification version 3.1 for the Rick and Morty API.
Ensure that there are no validation errors.
If any errors are found, fix them, then revalidate, repeat the last steps until the OpenAPI specification is valid.
```

Prompt 5

```
Using the API documentation found at https://wheretheiss.at/w/developer build an OpenAPI specification version 3.1 using the rules
1) ensure all operationIds use kebab case
2) add info and contact information using your details
3) ensure servers are defined
4) ensure all operations contains a description
5) ensure all operations have one or more relevant tags
6) ensure there is a tag section

Ensure that there are no validation errors.
If any errors are found, fix them, then revalidate, repeat the last steps until the OpenAPI specification is valid.
```

## Useful links

* [What is an MCP Server?⁠](https://www.anthropic.com/news/model-context-protocol)
* [MCP Spectral on Docker Hub](https://hub.docker.com/r/marksivill/mcp-spectral)
* [Spectral](https://stoplight.io/open-source/spectral) linter for OpenAPI specifications

