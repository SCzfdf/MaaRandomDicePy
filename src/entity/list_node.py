from src.entity.dice import Dice


class ListNode:
    def __init__(self, val: Dice, next=None):
        self.val: Dice = val
        self.next: ListNode = next


def list_to_circular_linkedlist(nums):
    """
    将列表转换为循环链表

    Args:
        nums: 输入列表

    Returns:
        ListNode: 循环链表的头节点
    """
    if not nums:
        return None

    # 创建头节点
    head = ListNode(nums[0])
    current = head

    # 构建链表
    for num in nums[1:]:
        current.next = ListNode(num)
        current = current.next

    # 将最后一个节点指向头节点，形成循环
    current.next = head

    return head