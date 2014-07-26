using CSharpTest.Net.Collections;
using CSharpTest.Net.Serialization;
using NetMQ;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;
using System.Threading.Tasks;

namespace LambdaManBoardUtil
{
    public class Program
    {
        static void Main(string[] args)
        {
            if (args != null && args.Length == 3)
            {
                // setup worker with args
            }
            else
            {
                var worker = new Worker("sample.json", "tcp://localhost:5557", "tcp://localhost:5558");

                worker.CalculateEverything();

                worker.DoWork();

                Console.WriteLine("whoah");
                Console.ReadKey();
            }
        }
    }

    public class Worker : IDisposable
    {
        string _pathToWork, _toAddress, _fromAddress;

        BPlusTree<uint, byte[]> _frames;
        public BPlusTree<uint, byte[]> Frames
        {
            get { return _frames; }
        }

        List<uint> _frameTickList;

        public Worker(string PathToWork,
                      string ToAddress,
                      string FromAddress)
        {
            _pathToWork = PathToWork;
            _toAddress = ToAddress;
            _fromAddress = FromAddress;

            // Stores the frames on the disk, since we probably will run out of ram.
            BPlusTree<uint, byte[]>.Options options = new BPlusTree<uint, byte[]>.Options(
                            PrimitiveSerializer.UInt32, PrimitiveSerializer.Bytes)
            {
                CreateFile = CreatePolicy.Always, // Always overwrite
                FileName = @"Storage.dat"
            };

            _frames = new BPlusTree<uint, byte[]>(options);

            _frameTickList = new List<uint>();
        }

        ~Worker()
        {
            if (_frames != null)
            {
                _frames.Dispose();
                _frames = null;
            }
        }

        public void Dispose()
        {
            if (_frames != null)
            {
                _frames.Dispose();
                _frames = null;
            }
        }

        public void CalculateEverything()
        {
            var random = new Random();
            var bf = new BinaryFormatter();

            foreach (var line in File.ReadLines(_pathToWork))
            {
                var boardFrame = JsonConvert.DeserializeObject<BoardFrame>(line);
                    
                MemoryStream ms = new MemoryStream();
                bf.Serialize(ms, boardFrame);

                var fakeTick = (uint)random.Next(int.MaxValue);

                _frames.Add(//boardFrame.TickNumber
                    fakeTick
                    , ms.ToArray());

                _frameTickList.Add(//boardFrame.TickNumber
                    fakeTick
                    );
                _frameTickList.Sort();
            }
            
        }

        public void DoWork()
        {
            using (var context = NetMQContext.Create())
            {
                using (NetMQSocket receiver = context.CreatePullSocket(),
                                   sender = context.CreatePushSocket())
                {
                    receiver.Connect(_fromAddress);
                    sender.Bind(_toAddress);
                    Console.WriteLine("connected");
                    System.Threading.Thread.Sleep(6000);
                    Console.WriteLine("sending");

                    sender.Send(JsonConvert.SerializeObject(new MessageFrame() { Type = "initResponse", Parameters = "wow server" }));

                    Console.WriteLine("sent");
                    while (true)
                    {
                        var rawRequest = receiver.ReceiveString();
                        Console.WriteLine("got request!");

                        var request = JsonConvert.DeserializeObject<MessageFrame>(rawRequest);

                        MessageFrame response = new MessageFrame();

                        switch(request.Type)
                        {
                            case "initRequest":
                            {
                                response.Type = "initResponse";
                                response.Parameters = JsonConvert.SerializeObject(_frameTickList);
                                break;
                            }
                        }

                        if (!string.IsNullOrWhiteSpace(response.Type))
                        {
                            var serialized = JsonConvert.SerializeObject(response);
                            Console.WriteLine("sending init response, \n" + serialized);
                            sender.Send(serialized);
                        }
                    }
                }
            }
        }

        private BoardFrame ReadFrameFromDB(uint tick)
        {
            if (_frames.ContainsKey(tick))
            {
                var serializedFrame = _frames[tick];

                MemoryStream memStream = new MemoryStream();
                BinaryFormatter binForm = new BinaryFormatter();
                memStream.Write(serializedFrame, 0, serializedFrame.Length);
                memStream.Seek(0, SeekOrigin.Begin);
                var frame = (BoardFrame)binForm.Deserialize(memStream);
                return frame;
            }

            return null;
        }
    }
}
