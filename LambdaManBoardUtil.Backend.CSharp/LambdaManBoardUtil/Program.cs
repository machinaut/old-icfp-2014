using NetMQ;
using System;
using System.Collections.Generic;
using System.Linq;
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
                var worker = new Worker("test.json", "tcp://localhost:5557", "tcp://localhost:5558");


            }
        }
    }

    public class Worker
    {
        string pathToWork, toAddress, fromAddress;

        public Worker(string PathToWork,
                      string ToAddress,
                      string FromAddress)
        {
            pathToWork = PathToWork;
            toAddress = ToAddress;
            fromAddress = FromAddress;
        }

        public void CalculateEverything()
        {

        }

        public void DoWork()
        {
            using (var context = NetMQContext.Create())
            {
                using (NetMQSocket receiver = context.CreatePullSocket(),
                                   sender = context.CreatePushSocket())
                {
                    receiver.Connect(fromAddress);
                    sender.Connect(toAddress);

                    // Allows us to remotely kill the process
                    while (true)
                    {
                        string taskString = receiver.ReceiveString();

                        var tasks = taskString.Split(',');

                        var job = tasks[0]; // First index is Job id

                        //var result = new JobResult(job);

                        //// Our 'work'
                        //foreach (var word in tasks.Skip(1).Distinct())
                        //{
                        //    result.Data[word] = tasks.Count(p => p == word);
                        //}

                        //var serializeMe = JsonConvert.SerializeObject(result);

                        //// Send 'result' to the sink
                        //sender.Send(serializeMe);
                    }
                }
            }
        }
    }
}
