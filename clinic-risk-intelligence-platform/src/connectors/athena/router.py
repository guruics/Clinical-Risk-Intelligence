class AthenaPracticeRouter:

    AMBULATORY = "195900"
    HOSPITAL = "1128700"
    PHR = "80000"

    def resolve(self, context: dict) -> str:
        """
        Determines which practice ID to use based on event context.
        """

        system_type = context.get("system_type")
        event_type = context.get("event_type")

        # PHR apps
        if system_type == "PHR":
            return self.PHR

        # hospital workflows
        if system_type == "HOSPITAL":
            return self.HOSPITAL

        # default → ambulatory
        return self.AMBULATORY