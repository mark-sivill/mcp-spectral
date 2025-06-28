#
# A Model Context Protocol (MCP) Server that lints/validates an
# OpenAPI specification using Spectral (https://stoplight.io/open-source/spectral)
# via commandline using Python
#

# build using FastMCP version 2 https://gofastmcp.com/
from fastmcp import FastMCP
from spectral_wrapper import SpectralWrapper
import json
from typing import Optional, Dict, Any
import sys
import traceback

mcp = FastMCP("openapi-specification-linting-with-spectral")

# set up access to Spectral linting tool
spectral = SpectralWrapper()

def __process_spectral_lint_result(result) -> Dict[str, Any]:

    try:

        if result.ok and result.ok.returncode == 0 and result.ok.stdout.startswith("[]"):
            lint_no_errors:  Dict[str, Any] = {
                "Lint Status": "No validation errors found"
            }
            return lint_no_errors
        
        elif result.ok and ( result.ok.returncode == 0 or result.ok.returncode == 1 ) :
            lint_with_errors:  Dict[str, Any] = {
                "Lint Status": "Some validation errors found",
                "Validation Errors": json.loads(result.ok.stdout)
            }
            return lint_with_errors

        elif result.err:
            unknown_error: Dict[str, Any] = {
                "Error": "Internal Model Context Protocol (MCP) server error",
                "err": result.err
            }
            return unknown_error       

        else:
            unknown_error: Dict[str, Any] = {
                "Unknown Error": "Unknown internal Model Context Protocol (MCP) server error",
                "returncode": result.ok.returncode,
                "stdout": result.ok.stdout,
                "stderr": result.ok.stderr,
                "args": result.ok.args,
            }
            return unknown_error
        
    except Exception:

        exc_type, exc_value, exc_traceback = sys.exc_info()
        unknown_error: Dict[str, Any] = {
            "Unknown Error": "Unknown internal Model Context Protocol (MCP) server error",
            "error_type": exc_type.__name__ if exc_type else None,
            "error_module": exc_type.__module__ if exc_type else None,
            "error_message": str(exc_value),
            "traceback_text": traceback.format_exc(),
            "traceback_list": traceback.format_tb(exc_traceback) if exc_traceback else [],            
        }
        return unknown_error

@mcp.tool()
def lint_openapi(openapi_specification) -> Dict[str, Any]:
    """Validate an OpenAPI specification"""
    result = spectral.lint(openapi_specification)
    return __process_spectral_lint_result(result)
#    if result.ok and result.ok.returncode == 0 and result.ok.stdout.startswith("[]"):
#        return json.loads("[]")
#    elif result.ok and result.ok.returncode == 1:
#        return json.loads(result.ok.stdout)
#    else:
#        return json.loads('{"Error": "Unknown internal Model Context Protocol (MCP) Server Error"}')
    
@mcp.tool()
def lint_openapi_with_ruleset(openapi_specification:str,spectral_ruleset:str) -> Dict[str, Any]:
    """Validate an OpenAPI specification using a ruleset"""
    result = spectral.lint(openapi_specification,spectral_ruleset)
    return __process_spectral_lint_result(result)
 #   if result.ok and result.ok.returncode == 0 and result.ok.stdout.startswith("[]"):
 #       return json.loads("[]")
 #   elif result.ok and result.ok.returncode == 1:
 #       return json.loads(result.ok.stdout)
 #   else:
 #       return json.loads('{"Error": "Unknown internal Model Context Protocol (MCP) Server Error"}')
    
@mcp.tool()
def spectral_version() -> str:
    """Get Spectral version"""
    version = spectral.version()
    if version.ok and version.ok.returncode == 0:
        result = version.ok.stdout
    else:
        result = "Error or Unknown"
    return result
    
if __name__ == "__main__":
   mcp.run()
