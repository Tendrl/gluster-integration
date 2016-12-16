from tendrl.common.atoms.base_atom import BaseAtom


class VolumeStopped(BaseAtom):
    def run(self, parameters):
        return True
