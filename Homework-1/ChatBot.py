
#%% [markdown]
# # Chatbot

#%% [markdown]
# Starting from some basic functions that may be required for Homework

#%% [markdown]
# ## Pattern match (From slides)
#%%
def is_variable(pat):
    """
    @pat: `string` string that could be a variable
    @return: 'bool', whether the input string is a variable
    """
    return pat.startswith('?') and all(s.isalpha() for s in pat[1:])


#%%
is_variable("?X")

#%%
def pat_match(pattern, saying):
    """
    @pattern: pattern string containing variables
    @saying: a saying string
    @return: tuple('string'), tuples of variables and matched words in saying
    """
    if is_variable(pattern[0]):
        return pattern[0], saying[0]
    else:
        if pattern[0] != saying[0]: return "",""
        else:
            return pat_match(pattern[1:], saying[1:])

#%%
pattern = "I want ?X".split()
saying = "I want holiday".split()
pat_match(pattern, saying)

#%%
def pat_match(pattern, saying):
    """
    modified `pattern match` function for multiple variables
    @pattern: `List(`string`)`, pattern string that contain variables
    @saying: `List(`string`)`, saying string that contain matched words
    @return: `List(tuple('string'))`, tuples that contain pair of variable and matched word
    """
    if not pattern or not saying: return []

    if is_variable(pattern[0]):
        return [(pattern[0], saying[0])] + pat_match(pattern[1:], saying[1:])
    else:
        if pattern[0] != saying[0]: return []
        else:
            return pat_match(pattern[1:], saying[1:])

#%%
pat_match("?X greater than ?Y".split(), "3 greater than 2".split())

#%%
def pat_to_dict(patterns):
    """
    suppose there is one-to-one correspondence between variable and word
    @patterns: `List(tuples(`string`))`, a list of `variable - word` pairs
    """
    return {k:v for k,v in patterns}

def substitute(rule, parsed_rules):
    """
    @rule: `list`, array of words including variables that may correspond to some words
    @parsed_rule: `dict`, mapping from 'rule' to 'words'
    @return: `list`, array of words where `variables` has been substituted by `word`
    """
    if not rule: return []
    return [parsed_rules.get(rule[0], rule[0])] + substitute(rule[1:], parsed_rules)

#%%
got_patterns = pat_match("I want ?X".split(), "I want iPhone".split())
substitute("What if you mean if you got a ?X".split(), pat_to_dict(got_patterns))
# or
join_pat = ' '.join(substitute("What if you mean if you got a ?X".split(), pat_to_dict(got_patterns)))

#%%
defined_patterns = {
    "I need ?X": ["Image you will get ?X soon", "Why do you need ?X ?"], 
    "My ?X told me something": ["Talk about more about your ?X", "How do you think about your ?X ?"]
}

def get_response(saying, rules):
    """" please implement the code, to get the response as followings:
    
    >>> get_response('I need iPhone') 
    >>> Image you will get iPhone soon
    >>> get_response("My mother told me something")
    >>> Talk about more about your monther.
    
    @saying: `string`, saying string having words
    @rules: `dict`, pre-defined responses for specific patterns
    @return: `string`, response string for a saying string according to `rules`
    """
    # find patterns in `rules` that match `saying`
    matched_pattern_rules = []
    for pat in rules:
        tmp = pat_match(pat.split(), saying.split())
        if not tmp: continue
        matched_pattern_rules.append((pat, tmp))
    
    # randomly picked one matched_pattern TODO: add random index
    matched_pattern, patterns = matched_pattern_rules[0]
    parsed_rule = pat_to_dict(patterns)

    # randomly picked one response pattern rule TODO: add random index
    response_pattern_rule = rules[matched_pattern][0]
    return substitute(response_pattern_rule.split(), parsed_rule)

#%%
test_saying = "I need iPhone"
get_response(test_saying, defined_patterns)

#%% [markdown]
### Segment Match (From slides)

#%% 
def is_pattern_segment(pattern):
    """
    determine whether a string is a segment variable
    @pattern: `string`, 
    """
    return pattern.startswith('?*') and all(a.isalpha() for a in pattern[2:])

#%%
is_pattern_segment("?*P")

#%%
def is_match(rest, saying):
    """
    @rest: `List(string)`, list of words
    @saying: `List(string)`, list of words
    @return: `bool`, whether two list of words matched each other
    """
    if not rest and not saying:
        return True
    if not all(a.isalpha() for a in rest[0]):
        return True
    if rest[0] != saying[0]:
        return False
    return is_match(rest[1:], saying[1:])

def segment_match(pattern, saying):
    """
    assume `pattern` string and `saying` string are same except `segment variable`
    @pattern: `List(string)`, list of words that starting with a variable
    @saying: `List(string)`, list of words that have words to which variables matched
    @return: `Tuple(tuple(string, List(string)), int)`, pair of `variable-segment of string pair` and its location
    """
    seg_pat, rest = pattern[0], pattern[1:]
    seg_pat = seg_pat.replace('?*', '?')
    if not rest: return (seg_pat, saying), len(saying)

    for i, token in enumerate(saying):
        if rest[0] == token and is_match(rest[1:], saying[(i+1):]):
            return (seg_pat, saying[:i]), i
    return (seg_pat, saying), len(saying)
    
#%%
fail = [True, None]

def pat_match_with_seg(pattern, saying):
    """
    @pattern: `List(`string`)`, a pattern string that would contain (segment) variables
    @saying: `List(`string`)`, a saying string that contain words to match `variables`
    @return: `List(tuple(string, List(string)))`
    """
    if not pattern or not saying: return []

    pat = pattern[0]
    
    if is_pattern_segment(pat):
        match, index = segment_match(pattern, saying)
        return [match] + pat_match_with_seg(pattern[1:], saying[index:])
    elif is_variable(pat):
        return [(pat, saying[0])] + pat_match_with_seg(pattern[1:], saying[1:])
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    else:
        return []

#%% 
segment_match('?*P is very good'.split(), "My dog and my cat is very good".split())
pat_match_with_seg('?*P is very good and ?*X'.split(), "My dog is very good and my cat is very cute".split())

#%%
response_pair = {
    "I need ?X": ["Why do you need ?X"], 
    "I don't like my ?X": ["What bad things did ?X do for you?"]
}
pat_match_with_seg('I need ?*X'.split(), 
                  "I need an iPhone".split())
substitute("Why do you neeed ?X".split(), pat_to_dict(pat_match_with_seg('I need ?*X'.split(), 
                  "I need an iPhone".split())))

#%% 
def pat_to_dict(patterns):
    """
    (modified)suppose there is one-to-one correspondence between variable and word
    @patterns: `List(tuples(`string`))`, a list of `variable - word` pairs
    """
    return {k:' '.join(v) if isinstance(v, list) else v for k,v in patterns}

substitute("Why do you neeed ?X".split(), pat_to_dict(pat_match_with_seg('I need ?*X'.split(), 
                  "I need an iPhone".split())))

#%% [markdown]
## Homework parts

#%% 
rules = {
    "?*X hello ?*Y": ["Hi, how do you do?"],
    "I was ?*X": ["Were you really ?X ?", "I already knew you were ?X ."]
}
#%% [markdown]
### Task 1
# Do modification to these three functions to make it work.

#%% 
import random
def segment_match(pattern, saying):
    """(modified: avoid starting variable match all words)
    assume `pattern` string and `saying` string are same except `segment variable`
    @pattern: `List(string)`, list of words that starting with a variable
    @saying: `List(string)`, list of words that have words to which variables matched
    @return: `Tuple(tuple(string, List(string)), int)`, pair of `variable-segment of string pair` and its location
    """
    seg_pat, rest = pattern[0], pattern[1:]
    seg_pat = seg_pat.replace('?*', '?')
    if not rest: return (seg_pat, saying), len(saying)
    
    for i, token in enumerate(saying):
        # assume the length of `rest` cannot exceed the length of saying
        if len(saying) - i - 1 < len(rest):
            break
        if rest[0] == token and is_match(rest[1:], saying[(i+1):]):
            return (seg_pat, saying[:i]), i
    return (seg_pat, saying[:i]), i

def pat_match_with_seg(pattern, saying):
    """(modified: add bool in @return to transmit `wrong flags` along recursion)
    @pattern: `List(`string`)`, a pattern string that would contain (segment) variables
    @saying: `List(`string`)`, a saying string that contain words to match `variables`
    @return: `List(tuple(string, List(string)), bool)`
    """
    if not pattern or not saying: return [True]

    pat = pattern[0]
    
    if is_pattern_segment(pat):
        match, index = segment_match(pattern, saying)
        tmp = pat_match_with_seg(pattern[1:], saying[index:])
        if not tmp[-1]:
            return [False]
        tmp.pop()
        return [match] + tmp + [True]
            
    elif is_variable(pat):
        tmp = pat_match_with_seg(pattern[1:], saying[1:]) 
        if not tmp[-1]:
            return [False]
        tmp.pop()
        return [(pat, saying[0])] + tmp + [True]
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    else:
        return [False]

def get_response(saying, rules):
    """(modified: add functions to gernerate responses (only for English))
    please implement the code, to get the response as followings:
    
    >>> get_response('I need iPhone') 
    >>> Image you will get iPhone soon
    >>> get_response("My mother told me something")
    >>> Talk about more about your monther.
    
    @saying: `string`, saying string having words
    @rules: `dict`, pre-defined responses for specific patterns
    @return: `string`, response string for a saying string according to `rules`
    """
    # find patterns in `rules` that match `saying`
    matched_pattern_rules = []
    for pat in rules:
        tmp = pat_match_with_seg(pat.split(), saying.split())
        if not tmp[-1]: continue
        tmp.pop()
        matched_pattern_rules.append((pat, tmp))
    print(matched_pattern_rules)
    # randomly picked one matched_pattern TODO: add random index
    matched_pattern, patterns = random.choice(matched_pattern_rules)
    parsed_rule = pat_to_dict(patterns)

    # randomly picked one response pattern rule TODO: add random index
    response_pattern_rule = random.choice(rules[matched_pattern])
    return substitute(response_pattern_rule.split(), parsed_rule)

#%%
# segment_match("?*P hello you".split(), "ABA dff hello you".split())
pat_match_with_seg("?*P hello you".split(), "ABA dff hello you".split())
segment_match("?*P hello you".split(), "ABA dff hello you".split())
print(" ".join(get_response("ABC hello <pad>", rules)))
print(" ".join(get_response("I was Yikang Yang", rules)))

#%% [markdown]
### Task 2
# Do modifications to `is_match`, `segment_match`, `pat_match_with_seg`, `get_response_jieba`
# add function `split` to split sentence that contain chinese characters.

#%%
import jieba
import random
import re

rules = {
    '?*x I want ?*y': ['what would it mean if you got ?y', 'Why do you want ?y', 'Suppose you got ?y soon'],
    '?*x if ?*y': ['Do you really think its likely that ?y', 'Do you wish that ?y', 'What do you think about ?y', 'Really-- if ?y'],
    '?*x你好?*y': ['你好呀', '请告诉我你的问题'],
    '?*x我想?*y': ['你觉得?y有什么意义呢？', '为什么你想?y', '你可以想想你很快就可以?y了'],
    '?*x我想要?*y': ['?x想问你，你觉得?y有什么意义呢?', '为什么你想?y', '?x觉得... 你可以想想你很快就可以有?y了', '你看?x像?y不', '我看你就像?y'],
    '?*x我是?*y': ['真的吗？', '?x想告诉你，或许我早就知道你是?y', '你为什么现在才告诉我你是?y']
}

seg_list = list(jieba.cut("我来到北京清华大学", cut_all=False))
print(list(seg_list))

def is_match(rest, saying):
    """(modified: add compatibility to Chinese)
    @rest: `List(string)`, list of words
    @saying: `List(string)`, list of words
    @return: `bool`, whether two list of words matched each other
    """
    if not rest and not saying:
        return True
    if not all(re.match('[\u4e00-\u9fa5]', a) is None and a.isalpha() for a in rest[0]):
        return True
    if rest[0] != saying[0]:
        return False
    return is_match(rest[1:], saying[1:])

def segment_match(pattern, saying):
    """(modified: add compatibility to Chinese)
    assume `pattern` string and `saying` string are same except `segment variable`
    @pattern: `List(string)`, list of words that starting with a variable
    @saying: `List(string)`, list of words that have words to which variables matched
    @return: `Tuple(tuple(string, List(string)), int)`, pair of `variable-segment of string pair` and its location
    """
    seg_pat, rest = pattern[0], pattern[1:]
    seg_pat = seg_pat.replace('?*', '?')
    if not rest: return (seg_pat, saying), len(saying)
    
    for i, token in enumerate(saying):
        # assume the length of `rest` cannot exceed the length of saying
        if len(saying) - i - 1 < len(rest):
            break
        if rest[0] == token and is_match(rest[1:], saying[(i+1):]):
            return (seg_pat, saying[:i]), i
    return (seg_pat, saying[:i]), i

def pat_match_with_seg(pattern, saying):
    """ (no updates)
    @pattern: `List(`string`)`, a pattern string that would contain (segment) variables
    @saying: `List(`string`)`, a saying string that contain words to match `variables`
    @return: `List(tuple(string, List(string)), bool)`
    """
    if not pattern or not saying: return [True]

    pat = pattern[0]
    
    if is_pattern_segment(pat):
        match, index = segment_match(pattern, saying)
        tmp = pat_match_with_seg(pattern[1:], saying[index:])
        if not tmp[-1]:
            return [False]
        tmp.pop()
        return [match] + tmp + [True]
            
    elif is_variable(pat):
        tmp = pat_match_with_seg(pattern[1:], saying[1:]) 
        if not tmp[-1]:
            return [False]
        tmp.pop()
        return [(pat, saying[0])] + tmp + [True]
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    else:
        return [False]


def split(chinese_seq):
    """ (new added: compatible for both chinese and English)
    split and merge
    @chinese_seq: `string`,seq of chinese characters but would have `variables`
    @return: `List(string)`, list of strings
    """
    lis = []
    l = r = 0
    seq = [re.match('[\u4e00-\u9fa5]', ch) is None for ch in chinese_seq] + [False]
    while l <= r and r <= len(chinese_seq):
        while r < len(chinese_seq) and seq[l] == seq[r]:
            r += 1
        if r == len(chinese_seq):
            lis.append(chinese_seq[l:r])
            break
        if seq[l] != seq[r]:
            lis.append(chinese_seq[l:r])
            l = r
    res = []
    for string in lis:
        tmp = re.match('[\u4e00-\u9fa5]+', string)
        if tmp:
            for word in jieba.cut(tmp.group(), cut_all=False):
                res.append(word)
        else:
            res += string.split()
    return res

def get_response_jieba(saying, rules):
    """ (modified: add compatiblity to Chinese)
    please implement the code, to get the response as followings:
    
    >>> get_response('I need iPhone') 
    >>> Image you will get iPhone soon
    >>> get_response("My mother told me something")
    >>> Talk about more about your monther.
    
    @saying: `string`, saying string having words
    @rules: `dict`, pre-defined responses for specific patterns
    @return: `string`, response string for a saying string according to `rules`
    """
    # find patterns in `rules` that match `saying`
    matched_pattern_rules = []
    for pat in rules:
        pattern = split(pat)
        saying_ = split(saying)
        tmp = pat_match_with_seg(pattern, saying_)
        if not tmp[-1]: continue
        tmp.pop()
        matched_pattern_rules.append((pat, tmp))
    
    # randomly picked one matched_pattern TODO: add random index
    matched_pattern, patterns = random.choice(matched_pattern_rules)
    parsed_rule = pat_to_dict(patterns)

    # randomly picked one response pattern rule TODO: add random index
    response_pattern_rule = random.choice(rules[matched_pattern])
    response_pattern_rule = split(response_pattern_rule)
    return substitute(response_pattern_rule, parsed_rule)

#%%
# make the algorithms compatible for both english and chinese
saying = "Hi我想玩游戏"
pattern = "?*x我想?*y"
# print(pat_match_with_seg(split(pattern), split(saying)))
print(get_response_jieba(saying, rules))

pattern = "?*x I want ?*y"
saying = "AA I want a new book"
# print(pat_match_with_seg(split(pattern), split(saying)))
print(get_response_jieba(saying, rules))

#%% [markdown]
### Task -3
# pass

#%% [markdown]
### Task -4
# 1. 优点： 
# * 针对规则以内出现的案例准确率高，机器人的回复会非常符合预设逻辑。
# * 在特定任务以及规则足够充分的情况下，机器人理论上可以做到足够智能而且稳定性强（参考游戏 《Red Dead: RedemptionⅡ》里的NPC）
# 2. 缺点： 
# * 预设规则之外的样例几乎不会成功
# * 即使是在规则之内，当遇到相似模式时候，程序无法有逻辑地选择匹配模式。
# * 程序回复只与当前问题本身有关，与之前的上下文无关。
# 3. 数据驱动：
# 个人认为数据驱动是一个理想概念，以可交互性机器人为例，我们预设好一个系统，里面包含预设的反馈方式及对应规则。人们通过输入数据或调参,
# 来让他达到用特定方式反馈特定信息，从而达到类似学习并最终到智能的效果。但真正意义上来说，这个机器更像是记下数据及经验，并不一定智能。
# 但是这个过程中人们并没有在对他系统核心方法进行额外的改进优化，唯一的变量只有输入的数据。
#
# 在这个程序中，我构建好了分词规则，模式选择（随机）, 以及信息提取方式（"？X", "?*X"），我们在这里的输入的数据是模式规则（rules）。
# 当我们为其输入的rules足够细分的时候，该程序能做到精确反馈人们的大部分信息。
#
# 4. 目前大部分AI的核心思想即为基于数据的经验主义模型。意思是模型本身不会思考不会类比，只是记住了得到正确答案的方式。而模型总结方式的过程
# 就是一次数据驱动的过程。主要关系为AI系统依赖于数据去“学习”如何解决复杂问题。

