from IPython.core.magic import Magics, magics_class, line_cell_magic
from IPython import get_ipython
import ast
import copy


class TQDMASTTransformer(ast.NodeTransformer):
    def visit_For(self, node):
        new_node = copy.deepcopy(node)
        new_node.iter = ast.Call(func=ast.Name(id='tqdm', ctx=ast.Load()),
                                 args=[node.iter], keywords=[])
        return new_node


@magics_class
class TQDMJupyter(Magics):
    _state = False

    @line_cell_magic
    def tqdm_jupyter(self, line):
        "Turn the autmatic TQDM in loops on and off"

        self._state = not self._state

        if self._state:
            self._install()
            print('tqdm magic installed')
        else:
            self._uninstall()
            print('tqdm magic uninstalled')

    def _install(self):

        self._uninstall()
        ip = get_ipython()
        ip.ast_transformers.append(TQDMASTTransformer())

    def _uninstall(self):

        ip = get_ipython()
        ip.ast_transformers = [t for t in ip.ast_transformers
                               if not isinstance(t, TQDMASTTransformer)]


def load_ipython_extension(ipython):
    ipython.register_magics(TQDMJupyter)
