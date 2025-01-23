import platform
import sysconfig

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):

    def initialize(self, version, build_data):
        # {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl
        build_data["tag"] = f"{self.python_tag()}-{self.python_tag()}-{sysconfig.get_platform().replace('-','_')}"
        return super().initialize(version, build_data)

    def python_tag(self):
        python_impl = platform.python_implementation()
        py_version_nodot = sysconfig.get_config_var("py_version_nodot")
        if python_impl == "CPython":
            return f"cp{py_version_nodot}"
        elif python_impl == "PyPy":
            return f"pp{py_version_nodot}"
        elif python_impl == "Jython":
            return f"jp{py_version_nodot}"
        elif python_impl == "IronPython":
            return f"ip{py_version_nodot}"
        else:
            return "py3"
