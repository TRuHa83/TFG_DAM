import argparse

class CustomFormatter(argparse.HelpFormatter):
    def _format_action(self, action):
        if isinstance(action, argparse._SubParsersAction):
            # Personaliza la presentación de subcomandos
            parts = []
            for name, subparser in action.choices.items():
                # Obtén el help del diccionario de metadatos de subparsers
                help_text = action._choices_actions[list(action.choices.keys()).index(name)].help or 'No description'
                parts.append(f"  {name:<15} {help_text}")

            if parts:
                return "\n".join(parts) + "\n"

            return ""

        if isinstance(action, argparse._HelpAction):
            return ""

        return super()._format_action(action)

    def _format_usage(self, usage, actions, groups, prefix):
        # Personaliza el formato del usage
        if prefix is None:
            prefix = 'usage: '

        return f"{prefix}{self._prog} COMMAND OPTIONS\n"
