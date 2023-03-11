def subset_to_shorthand(subset: str) -> str:
    if "#" in subset:
        return subset.split("#")[-1]
    else:
        return subset
