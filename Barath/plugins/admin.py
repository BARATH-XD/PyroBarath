import config
from pyrogram import filters, enums
from pyrogram.types import ChatPrivileges
from Barath import barath, MODULE


@barath.on_message(filters.command(["promote","fpromote"], prefixes=config.HANDLER) & filters.me)
async def promote_member(_, message):
     if message.reply_to_message:
          user_id = message.reply_to_message.from_user.id
     else:
        try:
           user_id = message.command[1]
        except:
            return await message.edit("Input username either id!")
     try:
         my_privileges = (await message.chat.get_member(user_id=message.from_user.id)).privileges 
         can_promote_members = [True if my_privileges and my_privileges.can_promote_members else False][0]
     except:
           return await message.edit("You aren't admin or you didn't have `can_promote_members` rights")
     command = message.command[0]
     if command == "fpromote" and can_promote_members:
              await message.chat.promote_member(user_id=user_id, privileges=my_privileges)
              return await message.edit("=> Fully Promoted!")
     elif command == "promote" and can_promote_members:
             privileges = ChatPrivileges(
                        can_delete_messages=True, can_restrict_members=True,
                        can_change_info=True, can_invite_users=True, can_pin_messages=True, can_manage_video_chats=True)
             await message.chat.promote_member(user_id=user_id, privileges=privileges)
             return await message.edit("=> Promoted!")
                     


@barath.on_message(filters.command(["pin","unpin"], prefixes=config.HANDLER) & filters.me)
async def messages_pin(_, message):
      if not message.reply_to_message:
           return await message.edit("No Reply?")
      else:
         try:
            command = message.text[1:].casefold()
         except Exception as e:
              return await message.edit_text(f"Somthing Wrong Happens:\n{e}")
         link = message.reply_to_message.link
         if command == "pin":    
             try:
                 await message.reply_to_message.pin()
             except Exception as e:
                 return await message.edit_text(f"Somthing Wrong Happens:\n{e}")
             return await message.edit(f"Successfully [Pinned]({link})!")
         elif command == "unpin":
               try:
                   await message.reply_to_message.unpin()
               except Exception as e:
                   return await message.edit_text(f"Somthing Wrong Happens:\n{e}")
               return await message.edit(f"Successfully [UnPinned]({link})")


@barath.on_message(filters.command("invite", prefixes=config.HANDLER) & filters.me)
async def invite_link(_, message):
     chat_id = message.chat.id
     try:
        link = (await barath.get_chat(chat_id)).invite_link
     except Exception as e: 
         return await message.edit(f"Somthing Wrong Happens:\n{e}")
     return await message.edit(str(link))

@barath.on_message(filters.command("admins", prefixes=config.HANDLER) & filters.me)
async def admins_list(_, message):
     chat_id = message.chat.id
     title = message.chat.title
     msg = await message.edit("Analyzing Admins...")
     mm = f"👮 Admins in {title}:\n"
     try:
        async for m in barath.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
              if m.user.is_bot != True:
                    mm += f"=> [{m.user.first_name}](tg://user?id={m.user.id})\n"
     except Exception as e:
           return await msg.edit(f"Somthing Wrong Happens:\n{e}")
     return await msg.edit(mm)
     

@barath.on_message(filters.command("del", prefixes=config.HANDLER) & filters.me)
async def delete_message(_, message):
     if message.reply_to_message:
         try:
            await message.reply_to_message.delete()
         except Exception as e:
              return await message.edit(f"Somthing wrong Happens:\n{e}")
         return await message.delete()
     else:
         return await message.edit("No Reply?")



@barath.on_message(filters.command("ban", prefixes=config.HANDLER) & filters.me)
async def ban_member(_, message):
    if message.reply_to_message:
         user_id = message.reply_to_message.from_user.id  
    else:
      try:
         user_id = message.text.split()[1]
      except:
          return await message.edit("Provide USER_ID To Ban!")
    try:
       owo = await message.chat.ban_member(user_id)
    except Exception as e:
        return await message.edit(f"Somthing wrong Happens:\n{e}")
    name = (await barath.get_users(user_id)).first_name
    return await message.edit(f"=> {name} Has Been Banned!")


@barath.on_message(filters.command("unban", prefixes=config.HANDLER) & filters.me)
async def unban_member(_, message):
    if message.reply_to_message:
         user_id = message.reply_to_message.from_user.id  
    else:
      try:
         user_id = message.text.split()[1]
      except:
          return await message.edit("Provide USER_ID To UnBan!")
    try:
       owo = await message.chat.unban_member(user_id)
    except Exception as e:
        return await message.edit(f"Somthing wrong Happens:\n{e}")
    name = (await barath.get_users(user_id)).first_name
    return await message.edit(f"=> {name} Has Been UnBanned!")


@barath.on_message(filters.command("purge", prefixes=config.HANDLER) & filters.me)
async def purge(_, message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        return await message.edit_text("No Reply?")
    else:
        reply_msg_id = message.reply_to_message.id
        message_id = message.id
        message_ids = []
        for ids in range(reply_msg_id, message_id):
            message_ids.append(ids)
        try:
           await barath.delete_messages(chat_id=chat_id, message_ids=message_ids)
        except Exception as e:
              return await message.edit(f"Somthing wrong Happens:\n{e}")
        return await message.edit(f"=> Purged {len(message_ids)} Messages")
       

__mod_name__ = "ADMIN"  
    
__help__ = """  
- promote: promote a member
- fpromote: full promote a member
- demote: demote a member
- admins: to get admin list
- purge: to delete 100msgs
- del: to delete 1msg
- ban: to ban member
- unban: to unban member
- pin: pin a message
- unpin: unpin a message
- invite: kidnap someone 
"""  
    
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)
