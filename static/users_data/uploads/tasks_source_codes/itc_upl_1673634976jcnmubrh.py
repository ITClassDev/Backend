def generate_hashtag(s):
    if not s:
        return False
    words = s.split()
    res = [i.capitalize() for i in words]
    cap = "".join(res)
    if len(cap) + 1 > 140:
        return false
    return f"#{cap}"

print(solution("x"))