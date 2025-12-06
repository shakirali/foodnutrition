
from spoon_ai.llm.interface import ProviderMetadata

def apply_patches():
    print("Applying ProviderMetadata patch...")
    original_init = ProviderMetadata.__init__

    def patched_init(self, name, version, capabilities, max_tokens=8192, supports_system_messages=False, rate_limits=None, **kwargs):
        # Check if 'requires_system_messages' was passed in kwargs (backward compatibility)
        if 'requires_system_messages' in kwargs:
             supports_system_messages = kwargs.pop('requires_system_messages')

        if rate_limits is None:
            rate_limits = {}

        # Call the original init with all required arguments
        # We interpret the signature seen on the system:
        # (self, name, version, capabilities, max_tokens, supports_system_messages, rate_limits)
        
        original_init(self, name, version, capabilities, max_tokens, supports_system_messages, rate_limits)

    ProviderMetadata.__init__ = patched_init
    print("ProviderMetadata patch applied.")
