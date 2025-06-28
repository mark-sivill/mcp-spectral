#
# direct wrapper over Spectral commandline allowing for following instructions
#
# 1) return Spectral version
# 2) lint an OpenAPI specification with optional ruleset
#

import shutil
import subprocess
import json
from typing import Optional, Dict, Any

import datetime
import random
import os
from pydantic import BaseModel, Field, ConfigDict

# structure used to return outcome of command line instruction
class SpectralResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    ok: Optional[subprocess.CompletedProcess] = Field(default=None)
    err: Optional[str] = Field(default=None)

class SpectralWrapper:

    # set up default values
    def __init__(self, spectral_command=None, default_ruleset=None ):

        # include Spectral path if needed
        self.spectral_command = spectral_command if spectral_command is not None else "spectral"

        # default ruleset file location
        self.default_ruleset = default_ruleset if default_ruleset is not None else "default-ruleset.yaml"

    # used to create a temporary working directory for OpenAPI files
    def __generate_working_directory(self) -> str:
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        random_number = random.randint(1000000, 9999999)
        return f"{timestamp}-{random_number}"
    
    # allow exception to be raised
    def __write_to_file(self, filename: str, content: str) -> None:
        with open(filename, 'w') as file:
            file.write(content)

    #
    # lint the openapi specifications using the default ruleset or provided ruleset
    # provide the specification/ruleset as the content itself
    #
    def lint(self, openapi_specification: str, spectral_ruleset: Optional[str] = None) -> SpectralResult:

        try:

            # create working directory
            working_directory = self.__generate_working_directory()
            os.makedirs(working_directory, exist_ok=True)
            openapi_specification_filename = f"{working_directory}/openapi-spec"
            spectral_ruleset_filename = f"{working_directory}/ruleset.yaml"

            #shutil.copy2(oas_file_path, openapi_spec )
            self.__write_to_file( openapi_specification_filename, openapi_specification )

            cmd = [self.spectral_command, "lint", openapi_specification_filename, "--format", "json"]

            if spectral_ruleset:
                self.__write_to_file( spectral_ruleset_filename, spectral_ruleset )
            else:
                shutil.copy2(self.default_ruleset, spectral_ruleset_filename )

            cmd.extend(["--ruleset", spectral_ruleset_filename])

            result = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            return SpectralResult(ok=result)
        
        except Exception as e:
            return SpectralResult(err=str(e))
        finally:
            # remove created filesworking directory
            shutil.rmtree(working_directory)

    #
    # return Spectral version
    #
    def version(self) -> SpectralResult:
        try:
            result = subprocess.run([self.spectral_command, "--version"], check=True, stdout=subprocess.PIPE, text=True)
            return SpectralResult(ok=result)
        except Exception as e:
            return SpectralResult(err=str(e))

